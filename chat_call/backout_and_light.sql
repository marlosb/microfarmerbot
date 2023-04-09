blackout luz blecaute escuro light

<|im_start|>O assistant procura pela data e hora, o número do potinho e a ação, que pode ser blackout ou luz, para inserir na tabela. Se faltar alguma dessas informações pergunte para o user.
A tabela chama-se seasons_table. Se a ação for blackout a data deve ser inserida na coluna blackout_date. Se a ação for luz a data deve ser inserida na coluna light_date.
O assistant retorna o código SQL para inserir os dados na tabela como nos exemplos abaixo.<|im_end|>

<|im_start|>user> dia 22/mar 8 horas: potinho 111 - blackout<|im_end|>
<|im_start|>assistent>
```
DECLARE @recent_season_id INT;

SELECT TOP 1 @recent_season_id = season_id 
FROM seasons_table 
WHERE container_id = 111 
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET blackout_date = '2023-03-22 08:00:00'
WHERE season_id = @recent_season_id;
```<|im_end|>

<|im_start|>user> dia 26/mar 19 horas: potinho 109 - blackout<|im_end|>
<|im_start|>assistent>
```
DECLARE @recent_season_id INT;

SELECT TOP 1 @recent_season_id = season_id 
FROM seasons_table 
WHERE container_id = 109 
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET blackout_date = '2023-03-26 19:00:00'
WHERE season_id = @recent_season_id;
```<|im_end|>

<|im_start|>user> dia 15/jun 07 horas: potinho 109 - luz<|im_end|>
<|im_start|>assistent>
```
DECLARE @recent_season_id INT;

SELECT TOP 1 @recent_season_id = season_id 
FROM seasons_table 
WHERE container_id = 109 
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET light_date = '2023-06-15 7:00:00'
WHERE season_id = @recent_season_id;
```<|im_end|>

<|im_start|>user> portinho 115 na luz dia 01/Abr as 8 horas<|im_end|>
<|im_start|>assistent>
```
DECLARE @recent_season_id INT;

SELECT TOP 1 @recent_season_id = season_id 
FROM seasons_table 
WHERE container_id = 115 
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET light_date = '2023-04-01 08:00:00'
WHERE season_id = @recent_season_id;
```<|im_end|>

<|im_start|>user> blackout para o potinho 154 as 3 horas do dia 2 de novembro<|im_end|>
<|im_start|>assistent>
```
DECLARE @recent_season_id INT;

SELECT TOP 1 @recent_season_id = season_id 
FROM seasons_table 
WHERE container_id = 154 
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET blackout_date = '2023-11-02 03:00:00'
WHERE season_id = @recent_season_id;
```<|im_end|>

<|im_start|>user> dia 14/jun, horas: potinhos 127 - blackout<|im_end|>
<|im_start|>assistent> Não foi informada a hora, qual a hora?<|im_end|>

<|im_start|>user> dia 18/mar, 7 horas: potinhos 113, 114 e 115 - blackout<|im_end|>
<|im_start|>assistent>
```
DECLARE @recent_season_id_113 INT, @recent_season_id_114 INT, @recent_season_id_115 INT;

SELECT TOP 1 @recent_season_id_113 = season_id 
FROM seasons_table 
WHERE container_id = 113 
ORDER BY plant_date DESC;

SELECT TOP 1 @recent_season_id_114 = season_id 
FROM seasons_table 
WHERE container_id = 114
ORDER BY plant_date DESC;

SELECT TOP 1 @recent_season_id_115 = season_id 
FROM seasons_table 
WHERE container_id = 115 
ORDER BY plant_date DESC;

UPDATE seasons_table 
SET blackout_date = '2023-03-18 07:00:00'
WHERE WHERE container_id IN (113, 114, 115)
AND season_id IN (@recent_season_id_113, recent_season_id_114, recent_season_id_115;)
```<|im_end|>