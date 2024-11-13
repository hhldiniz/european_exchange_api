module "cache_database" {
  source = "./modules/aws/dynamo"
  hash_key = "timestamp"
  table_name = "Cache"
  hash_key_type = "N"
  write_capacity = 25
  read_capacity = 25
}