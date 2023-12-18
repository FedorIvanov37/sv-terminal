# UBC-1096

## Description

Add region for card transaction

If transaction processed in "home" region - type equal Domestic, else - International.

Main condition for defining the region:

    if `transaction.merchant_country` == null -> `transaction.region` = null
      else if `transaction.merchant_country` == `partner_products.main_country` OR `transaction.merchant_country` in `partner_products.domestic_countries` -> `transaction.region` = Domestic
      else `transaction.region` = International

(!) Parameter will be affect the transaction fee.

## Solution

### DB

- (0) Add a table-dictionary `dict_country` of available BAAS countries ISO 3166-1

| name       | type    | nullable | pkey | example |
| ---------- | ------- | -------- | ---- | ------- |
| id         | int     | false    | true | 1       |
| name       | string  | false    |      | Cyprus  |
| alpha_2    | string  | false    |      | CY      |
| alpha_3    | string  | false    |      | CYP     |
| numeric    | int     | false    |      | 196     |
| is_default | boolean | false    |      | true    |

- In `transaction` table add:
  - (1) `transaction.merchant_country` (string\nullable) merchant country from transaction. Foreign key `dict_country.id`
    - for RHA protocol - 43.2
    - for messages from rabbitmq - merchant_country
  - (2) `transaction.region` (string\nullable) - the ratio of merchant country `transaction.merchant_country` to product home countries `partner_products.domestic_countries`. (!) Set a restriction on permissible values: **International**, **Domestic**, **null**
- In `partner_products` table add:
  - (3) `partner_products.main_country` (int\not null) - product country. Foreign key `dict_country.id`
  - (4) `partner_products.domestic_countries` (array[string]\not null) - list of foreign keys to `dict_country.id`

### Dashboard

When create  the product, need to add:

- define product country (3). Selected from the dropdown list with a search by entering the country name or code. If no list is specified, the default list is used.
- specifying the list of countries of the "home region" (4). Selected from the dropdown list with a search by entering the country name or code. If no list is specified, the default list is used.

### API

Add `transaction_region` (string, enum: International, Domestic, null)

- **TRANSACTION_INFO** webhook - `transaction.region`
- **card-transaction-changed** webhook - `transaction.region`
- **/cards/cardId/transactions** endpoint - `transaction.region`
- **/accounts/accountId/transactions** endpoint - `data.card_meta.transaction_region`

### Process

- When starting a product, the country (3) and the "home country list" (region) of the product (4) are specified. If no home region is specified - the default list (region) is used
- When a transaction is received, the merchant country (1) is retrieved and saved as a transaction attribute in the db
  - for RHA protocol - 43.2
  - for messages from rabbitmq - merchant_country
- Execute condition:
  - if (1) == null -> (2) = null
  - else if (1) == (3) OR (1) in (4) -> (2) = Domestic
  - else (2) = International
- The comparison result is saved as a transaction attribute in the database (2)

Condition with objects:

    if `transaction.merchant_country` == null -> `transaction.region` = null
      else if `transaction.merchant_country` == `partner_products.main_country` OR `transaction.merchant_country` in `partner_products.domestic_countries` -> `transaction.region` = Domestic
      else `transaction.region` = International