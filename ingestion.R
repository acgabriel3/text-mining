library(dplyr)
library(udpipe)
library(pdftools)
library(elastic)
library(httr)
library(data.table)

#***
#Criando operador para concatenacao de strings (utilizado para facilitar legibilidade de meta programacao)
'%%' <- function(a,b) paste0(a,b)

data <- read.csv("dados/sbrt/dados/sbrt_respostas_sentencas2.csv", encoding = "utf-8")

conn <- connect(host = "localhost", port = "9200")

index_name <- "sentencas_sbrt"

index_delete(conn = conn, index = index_name)

index_create(conn = conn, index = index_name)

mapping <- 
'
{
  "properties": {
    "senteca": {
      "type": "text"
    },
    "documento": {
      "type": "keyword"
    }
  }
}
'

mapping_create(conn = conn, index = index_name, body = mapping)

for (i in 1:nrow(data)){
  #Gravanddo as sentenças no banco de dados
      
  print(i)
  
  content <- '
    {
      "sentenca":' %% '"' %% as.character(data$sentenca) %% '"' %% ',
      "documento":' %% data$doc_id[1] %% '
    }
  '
      
  try(
    expr =   print(docs_create(conn = conn, index = index_name, body = content, type = "_doc"))
  )

}

#***
#exemplo de query:
# GET /sentencas_sbrt/_search?
# {
#   "query": {
#     "match": {
#       "sentenca": "sexo"
#     }
#   }
# }



















