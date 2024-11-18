module "cache_database" {
  source = "./modules/aws/dynamo"
  hash_key = "timestamp"
  table_name = "Cache"
  hash_key_type = "N"
  write_capacity = 25
  read_capacity = 25
}

module "currency_database" {
  source = "./modules/aws/dynamo"
  hash_key = "currency_code"
  table_name = "Currency"
  hash_key_type = "S"
  write_capacity = 25
  read_capacity = 25
}