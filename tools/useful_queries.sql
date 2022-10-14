-- Get all Gaia DR3 sources inside tile 411 as defined by its galactic coordinates.
SELECT *
FROM gaiadr3.gaia_source
WHERE l >= 5.0128 AND l <= 6.5309 AND b >= -14.5977 AND b <= -13.3988


-- Get all Gaia DR2 RR Lyrae inside tile 411 as defined by its galactic coordinates.
SELECT * 
FROM gaiadr2.vari_rrlyrae RR
    LEFT JOIN gaiadr2.gaia_source as GS 
        ON RR.source_id = GS.source_id
WHERE GS.l >= 5.0128 AND GS.l <= 6.5309 AND GS.b >= -14.5977 AND GS.b <= -13.3988 