library(readtext)
library(stringr)
library(dplyr)
library(qdap)
library(tm)

dossies_url <- paste0("dados", "/sbrt_txts/dossies/*.txt")

textos <- readtext(dossies_url)

textos_tratados <- c()
for (texto_dossie in textos$text) {
  texto_dossie_tratado <- texto_dossie %>%
    stringr::str_replace_all("\\r\\n", "\\n") %>%
    stringr::str_replace_all(
      "Copyright © Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.sbrt.ibict.br",
      ""
    ) %>%
    stringr::str_replace_all("\\s+", " ") %>%
    trimws()

  textos_tratados <- textos_tratados %>%
    append(texto_dossie_tratado)
}

text_corpus <- VCorpus(VectorSource(textos_tratados)) %>%
  tolower() %>%
  removePunctuation() %>%
  removeNumbers() %>%
  stripWhitespace() %>%
  removeWords(stopwords(kind = "portuguese")) %>%
  stringr::str_replace_all("\\s+", " ") %>%
  trimws()

text_corpus[[1]]
