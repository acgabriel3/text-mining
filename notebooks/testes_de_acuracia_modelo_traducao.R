library(dplyr)
library(data.table)
library(stringi)
library(vwr)

model_29_repetitions_four_tops <- fread("model_39_repetitions_top_words_and_four_tops.csv")
model_29_repetitions_four_tops_without <- fread("model_39_repetitions_top_words_and_four_tops_without_header_sbrt.csv")
model_four_tops_without_sbrt <- fread("model_four_tops_without_header_sbrt.csv")
model_without_batch_size <- fread("modelwithoutbatchsize.csv")

results <- levenshtein.distance(model_without_batch_size$V3, model_without_batch_size$V4)

model_without_batch_size$proximidade <- results


model_four_tops_without_sbrt <- model_without_batch_size %>%
                                  arrange(proximidade)

print("model_without_batch_size")
sum(results < 30, na.rm = TRUE)/nrow(model_without_batch_size) * 100

results <- levenshtein.distance(model_four_tops_without_sbrt$V3, model_four_tops_without_sbrt$V4)

model_four_tops_without_sbrt$proximidade <- results


model_four_tops_without_sbrt <- model_four_tops_without_sbrt %>%
  arrange(proximidade)

print("model_four_tops_without_sbrt")
sum(results < 30, na.rm = TRUE)/nrow(model_four_tops_without_sbrt) * 100


results <- levenshtein.distance(model_29_repetitions_four_tops_without$V3, model_29_repetitions_four_tops_without$V4)

model_29_repetitions_four_tops_without$proximidade <- results


model_29_repetitions_four_tops_without <- model_29_repetitions_four_tops_without %>%
  arrange(proximidade)

print("model_29_repetitions_four_tops_without")
sum(results < 30 * 0.4, na.rm = TRUE)/nrow(model_29_repetitions_four_tops_without) * 100

results <- levenshtein.distance(model_29_repetitions_four_tops$V3, model_29_repetitions_four_tops$V4)

model_29_repetitions_four_tops$proximidade <- results


model_29_repetitions_four_tops <- model_29_repetitions_four_tops %>%
  arrange(proximidade)

print("model_29_repetitions_four_tops")
sum(results < 30 * 0.4, na.rm = TRUE)/nrow(model_29_repetitions_four_tops) * 100

