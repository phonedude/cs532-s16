DROP TABLE IF EXISTS feed;
DROP TABLE IF EXISTS feature_count;
DROP TABLE IF EXISTS category_count;

CREATE TABLE IF NOT EXISTS feed(
num integer,
entry text,
feature text,
predicted text,
actual text,
cprob decimal
);

CREATE TABLE IF NOT EXISTS feature_count(
  feature  text,
  category text,
  count integer
);

CREATE TABLE IF NOT EXISTS category_count(
  category text,
  count integer
);

delete from feed;
delete from feature_count;
delete from category_count;