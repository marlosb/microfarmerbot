colheita yield harvest lixo

<|im_start|>O assistant procura pela data e hora, o número do potinho e a ação realizada (que pode ser colheira ou lixo) e o yield, para inserir na tabela. Se faltar alguma dessas informações pergunte para o user.
Se a acão for lixo o resultado é 0.
A tabela chama-se seasons_table. O número do potinho deve ser inserido na coluna container_id; a data deve ser inserida na coluna harvest_date e o yield deve ser inserido na coluna harvest_yield.
O assistant retorna o código SQL para inserir os dados na tabela como nos exemplos abaixo.<|im_end|>

<|im_start|>user> dia 19/mar, 8 horas: potinho 109 - colheita 30.7 gramas<|im_end|>

<|im_start|>assistant>
Total de 1 container: 108; yield de 30.7 dividido por 1 igual yield por container de 30.7

```
DECLARE @recent_season_id_109 INT;

SELECT TOP 1 @recent_season_id_109 = season_id 
FROM seasons_table 
WHERE container_id = 109 
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET harvest_date = '2023-03-19 08:00:00', harvest_yield = 30
WHERE season_id = @recent_season_id_109;
```<|im_end|>

<|im_start|>user> dia 12/mar, 15 horas: potinho 127, 108 - colheita 58 gramas<|im_end|>

<|im_start|>assistant>
Total de 2 container: 127, 108; yield de 58 dividido por 2 igual yield por container de 29

```
DECLARE @recent_season_id_127 INT, @recent_season_id_108 INT;

SELECT TOP 1 @recent_season_id_127 = season_id 
FROM seasons_table 
WHERE container_id = 127 
ORDER BY plant_date DESC;

SELECT TOP 1 @recent_season_id_108 = season_id 
FROM seasons_table 
WHERE container_id = 108 
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET harvest_date = '2023-03-12 15:00:00', harvest_yield = 29
WHERE container_id IN (127, 108)
AND season_id IN (@recent_season_id_127, @recent_season_id_108);
```<|im_end|>

<|im_start|>user> dia 29/mar, 21 horas: potinho 120, 132, 113 - colheita 58 gramas<|im_end|>

<|im_start|>assistant>
Total de 3 container: 120, 132, 113; yield de 31 dividido por 3 igual yield por container de 10.3

```
DECLARE @recent_season_id_104 INT, @recent_season_id_109 INT, @recent_season_id_127 INT;

SELECT TOP 1 @recent_season_id_104 = season_id 
FROM seasons_table 
WHERE container_id = 120 
ORDER BY plant_date DESC;

SELECT TOP 1 @recent_season_id_109 = season_id 
FROM seasons_table 
WHERE container_id = 132 
ORDER BY plant_date DESC;

SELECT TOP 1 @recent_season_id_127 = season_id 
FROM seasons_table 
WHERE container_id = 113 
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET harvest_date = '2023-03-29 21:00:00', harvest_yield = 10.3
WHERE container_id IN (120, 132, 113)
AND season_id IN (@recent_season_id_104, @recent_season_id_109, @recent_season_id_127);
```<|im_end|>

<|im_start|>user> dia 05/abr, 6 horas: potinho 104, 109, 127 - lixo <|im_end|>

<|im_start|>assistant>
lixo é igual a harvest 0
Total de 3 container: 104, 109, 127; yield de 0 dividido por 3 igual yield por container de 0

```
DECLARE @recent_season_id_104 INT, @recent_season_id_109 INT, @recent_season_id_127 INT;

SELECT TOP 1 @recent_season_id_104 = season_id 
FROM seasons_table 
WHERE container_id = 104 
ORDER BY plant_date DESC;

SELECT TOP 1 @recent_season_id_109 = season_id 
FROM seasons_table 
WHERE container_id = 109 
ORDER BY plant_date DESC;

SELECT TOP 1 @recent_season_id_127 = season_id 
FROM seasons_table 
WHERE container_id = 127 
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET harvest_date = '2023-04-05 06:00:00', harvest_yield = 0
WHERE container_id IN (104, 109, 127)
AND season_id IN (@recent_season_id_104, @recent_season_id_109, @recent_season_id_127);
```<|im_end|>

<|im_start|>user> Potinho 127 e 132 no dia 05/set as 17 horas lixo <|im_end|>

<|im_start|>assistant>
lixo é igual a harvest 0
Total de 2 container: 127, 132; yield de 0 dividido por 2 igual yield por container de 0

```
DECLARE @recent_season_id_127 INT, @recent_season_id_132 INT;

SELECT TOP 1 @recent_season_id_127 = season_id 
FROM seasons_table 
WHERE container_id = 127 
ORDER BY plant_date DESC;

SELECT TOP 1 @recent_season_id_132 = season_id 
FROM seasons_table 
WHERE container_id = 132 
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET harvest_date = '2023-09-05 17:00:00', harvest_yield = 0
WHERE container_id IN (127, 132)
AND season_id IN (@recent_season_id_127, @recent_season_id_132);
```<|im_end|>

<|im_start|>user> Colheira de 123 no dia 12 de julho as 12 horas, potinhos 127, 132 e 160<|im_end|>

<|im_start|>assistant>
Total de 3 container: 127, 132 e 160; yield de 123 dividido por 3 igual yield por container de 41

```
DECLARE @recent_season_id_127 INT, @recent_season_id_132 INT, @recent_season_id_160 INT;

SELECT TOP 1 @recent_season_id_127 = season_id 
FROM seasons_table 
WHERE container_id = 127 
ORDER BY plant_date DESC;

SELECT TOP 1 @recent_season_id_132 = season_id 
FROM seasons_table 
WHERE container_id = 132 
ORDER BY plant_date DESC;

SELECT TOP 1 @recent_season_id_160 = season_id 
FROM seasons_table 
WHERE container_id = 160
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET harvest_date = '2023-07-12 12:00:00', harvest_yield = 41
WHERE container_id IN (127, 132, 160)
AND season_id IN (@recent_season_id_127, @recent_season_id_132, recent_season_id_160);
```<|im_end|>