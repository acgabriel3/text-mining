library(stringr)
library(pdftools)
library(tm)

# you can use an url or a path
pdf_url <- "./dados/teste.pdf"

# `pdf_text` converts it to a list
list_output <- pdftools::pdf_text(pdf_url)
num_paginas <- length(list_output)

# list_output[[1]]

list_output <- lapply(list_output, function (pageText) {
  pageText <- as.character(pageText) %>%
    stringr::str_replace_all('\\r?\\n|\\r', ' ') %>%
    stringr::str_replace_all(
      'Copyright © Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.sbrt.ibict.br',
      ''
    ) %>%
    stringr::str_replace_all('DOSSIÊ TÉCNICO', '') %>%
    stringr::str_replace_all('\\s+', ' ') %>%
    stringr::str_replace_all('\\.+', '') %>%
    stringr::str_replace_all('_+\\s+\\d+?', '') %>%
    stringr::str_replace_all(' . ', ' ') %>%
    trimws()
  return(paste("<INICIO_PAGINA>", pageText, "<FIM_PAGINA>"))
})

# list_output[[1]]

# junta todas as pï¿½ginas do PDF lido
texto <- paste(unlist(list_output), collapse = ' ')

text_corpus <- tm::VCorpus(tm::VectorSource(texto)) %>%
  tolower() %>%
  tm::removePunctuation() %>%
  tm::removeNumbers() %>%
  tm::stripWhitespace() %>%
  tm::removeWords(c(stopwords(kind = "portuguese"), 'iniciopagina', 'fimpagina')) %>%
  stringr::str_replace_all('\\s+', ' ')
