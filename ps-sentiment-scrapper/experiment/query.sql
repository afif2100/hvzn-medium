SELECT "reviewId", "content"
FROM review
WHERE "reviewId" not in (SELECT "reviewId" from sentiment );
-- LIMIT 100;


SELECT Count("reviewId") as review_count from sentiment;

SELECT "review"."reviewId"
, "review"."score"
, "review"."content"
, "sentiment"."sentiment"

FROM review
LEFT JOIN sentiment
ON ("review"."reviewId"="sentiment"."reviewId")

order by RANDOM ()
LIMIT 100
;

DELETE FROM review 
WHERE "at" >= '2022-10-03 00:00:00';

SELECT "reviewId", COUNT("at")
from review
GROUP BY 1 HAVING COUNT(*) > 1;

DELETE  FROM
    review a
        USING review b
WHERE
    a."index" > b."index"
    AND a."reviewId" = b."reviewId";


-- Delete invalid review
SELECT * from sentiment
LEFT join review
ON "sentiment"."reviewId" = "review"."reviewId"
WHERE "review"."reviewId" is NULL;


DELETE FROM sentiment 
WHERE "reviewId"
in (SELECT "sentiment"."reviewId" from sentiment
	LEFT join review
	ON "sentiment"."reviewId" = "review"."reviewId"
	WHERE "review"."reviewId" is NULL
	);