file_conllu <- "pt_bosque-ud-train.conllu"

library(udpipe)
m <- udpipe_train(file = "lemmatizer_model.udpipe", files_conllu_training = file_conllu, 
                  annotation_tokenizer = list(dimension = 16, 
                                              epochs = 1, 
                                              batch_size = 100, 
                                              dropout = 0.7),
                  annotation_tagger = list(guesser_suffix_rules_2 = 6, 
                                           guesser_enrich_dictionary_2 = 4, 
                                           guesser_prefixes_max_2 = 4, 
                                           use_lemma_2 = 1, use_xpostag_2 = 0, 
                                           use_feats_2 = 0, 
                                           provide_lemma_2 = 1, 
                                           provide_xpostag_2 = 0, 
                                           provide_feats_2 = 0, 
                                           prune_features_2 = 0), 
                  annotation_parser = "none")



#carrega o modelo.
ud_model <- udpipe_load_model(m$file_model)
#Faz anotação com base no modelo
x <- udpipe_annotate(ud_model, x = txt)
x <- as.data.frame(x)