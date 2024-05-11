-- Rank country origins of bands by the number of (non-unique) fans
SELECT mb.origin, SUM(sfd.fan_count) AS nb_fans
FROM metal_bands mb
JOIN sample_fan_data sfd ON mb.id = sfd.band_id
GROUP BY mb.origin
ORDER BY nb_fans DESC;
