WITH

inflow AS (
  SELECT
    TO_ADDRESS AS address
    ,SUM(AMOUNT) AS value
  FROM
    gnosis.core.ez_token_transfers
  WHERE 
    CONTRACT_ADDRESS = '0xaf204776c7245bf4147c2612bf6e5972ee483701'
    AND
    BLOCK_TIMESTAMP <= '2024-07-14 18:00:00.000'
  GROUP BY 1
),

outflow AS (
  SELECT
    FROM_ADDRESS AS address
    ,-SUM(AMOUNT) AS value
  FROM
    gnosis.core.ez_token_transfers
  WHERE 
    CONTRACT_ADDRESS = '0xaf204776c7245bf4147c2612bf6e5972ee483701'
    AND
    BLOCK_TIMESTAMP <= '2024-07-14 18:00:00.000'
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
    gnosis.core.dim_labels
  WHERE
    label_type IN ('dex', 'cex', 'bridge', 'flotsam', 'defi')
)

SELECT 
  address
FROM addresses 
WHERE
  address NOT IN (SELECT address FROM exclude_addresses)
