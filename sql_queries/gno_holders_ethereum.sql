WITH

inflow AS (
  SELECT
    TO_ADDRESS AS address
    ,SUM(AMOUNT) AS value
  FROM
    ethereum.core.ez_token_transfers
  WHERE 
    CONTRACT_ADDRESS = '0x6810e776880c02933d47db1b9fc05908e5386b96'
    AND
    DATE(BLOCK_TIMESTAMP) <= '2024-06-04'
  GROUP BY 1
),

outflow AS (
  SELECT
    FROM_ADDRESS AS address
    ,-SUM(AMOUNT) AS value
  FROM
    ethereum.core.ez_token_transfers
  WHERE 
    CONTRACT_ADDRESS = '0x6810e776880c02933d47db1b9fc05908e5386b96'
    AND
    DATE(BLOCK_TIMESTAMP) <= '2024-06-04'
  GROUP BY 1
),

final_balance AS (
  SELECT
    address
    ,SUM(value) AS balance
  FROM (
    SELECT * FROM inflow
    UNION ALL 
    SELECT * FROM outflow
  )
  GROUP BY address 
),

addresses AS (
 SELECT * FROM final_balance
  WHERE balance > 0
),

exclude_addresses AS (
  SELECT DISTINCT
    address
  FROM
    ethereum.core.dim_labels
  WHERE
    label_type IN ('dex', 'cex', 'bridge', 'flotsam', 'defi')
)

SELECT 
  address
FROM addresses 
WHERE
  address NOT IN (SELECT address FROM exclude_addresses)
  AND
  address != '0x000000000000000000000000000000000000dead'