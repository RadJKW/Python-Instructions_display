-- @BLOCK@
-- create machine 112 

    INSERT INTO machines (
        id,
        division,
        host_name,
        host_ip,
        host_type,
        active,
        last_updated
      )
    VALUES (
        102,
        3,
        'cw-102',
        '10.11.18.62',
        'RPI',
        1,
        NOW()
      );

-- @BLOCK@
-- show me all the coil_data for operator 10001 and machine 83

    SELECT *
      FROM coil_data
      WHERE operator_id = 10001
        AND machine_id = 83
      ORDER BY coil_data.id;


-- @BLOCK@
-- create a new VIEW for Operator 10001,
-- the view will show all the machines associated with that operator
-- and how many unique coil_data.coil_numbers for each machine CREATE

    CREATE VIEW operator_10001 AS
      SELECT operators.*, coil_data.machine_id,
             COUNT(DISTINCT coil_data.coil_number) AS coil_count
        FROM operators
        LEFT JOIN coil_data
          ON coil_data.operator_id = operators.id
        WHERE operators.id = 10001
        GROUP BY coil_data.machine_id;


-- @BLOCK@
-- create a view that has the following collumns:
-- operator_id, operator_name, machine_id, coil_count, 
-- coil_count: is the sum of Unique coil_numbers for each operator_id CREATE
    
    CREATE VIEW operator_coil_count AS
      SELECT operators.id AS operator_id,
             operators.name AS operator_name,
             coil_data.machine_id,
             COUNT(DISTINCT coil_data.coil_number) AS coil_count
        FROM operators
        LEFT JOIN coil_data
          ON coil_data.operator_id = operators.id
        GROUP BY coil_data.machine_id;

            

-- @BLOCK@
DROP VIEW operator_coil_count; 

