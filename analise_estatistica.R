# FarmTech Solutions - estatística básica dos dados exportados pelo Python

args <- commandArgs(trailingOnly = TRUE)
argumento_arquivo <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
diretorio_script <- if (length(argumento_arquivo) > 0) {
  dirname(normalizePath(sub("^--file=", "", argumento_arquivo[1])))
} else {
  getwd()
}
arquivo <- if (length(args) >= 1) args[1] else file.path(diretorio_script, "dados_plantio.csv")

if (!file.exists(arquivo)) {
  stop("Arquivo não encontrado: ", arquivo, "\nExecute primeiro o programa Python e exporte o CSV.")
}

dados <- read.csv(arquivo, stringsAsFactors = FALSE, encoding = "UTF-8")
campos_obrigatorios <- c(
  "talhao", "cultura", "area_m2", "area_ha", "numero_ruas",
  "numero_plantas", "quantidade_insumo_kg"
)
faltantes <- setdiff(campos_obrigatorios, names(dados))
if (length(faltantes) > 0) {
  stop("Colunas obrigatórias ausentes: ", paste(faltantes, collapse = ", "))
}
if (nrow(dados) == 0) stop("O CSV não possui registros para análise.")

colunas_numericas <- c(
  "area_m2", "area_ha", "numero_ruas", "numero_plantas", "quantidade_insumo_kg"
)
for (coluna in colunas_numericas) {
  dados[[coluna]] <- as.numeric(gsub(",", ".", dados[[coluna]], fixed = TRUE))
}

estatisticas <- function(x) {
  x <- x[is.finite(x)]
  c(
    registros = length(x),
    media = mean(x),
    mediana = median(x),
    desvio_padrao = if (length(x) > 1) sd(x) else NA_real_,
    minimo = min(x),
    maximo = max(x)
  )
}

mostrar_linha <- function(rotulo, valores, unidade) {
  cat(sprintf(
    "%-18s média=%10.3f | mediana=%10.3f | desvio=%10.3f | mín=%10.3f | máx=%10.3f %s\n",
    rotulo, valores["media"], valores["mediana"], valores["desvio_padrao"],
    valores["minimo"], valores["maximo"], unidade
  ))
}

cat("\n============================================================\n")
cat(" FARMTECH SOLUTIONS - ANÁLISE ESTATÍSTICA\n")
cat("============================================================\n")
cat("Arquivo:", normalizePath(arquivo), "\n")
cat("Registros:", nrow(dados), "\n\n")

cat("RESUMO GERAL\n")
mostrar_linha("Área", estatisticas(dados$area_ha), "ha")
mostrar_linha("Plantas", estatisticas(dados$numero_plantas), "unid.")
mostrar_linha("Insumo", estatisticas(dados$quantidade_insumo_kg), "kg")

cat("\nRESUMO POR CULTURA\n")
resultados <- list()
for (cultura_atual in unique(dados$cultura)) {
  grupo <- dados[dados$cultura == cultura_atual, ]
  cat("\n--", cultura_atual, "--\n")
  mostrar_linha("Área", estatisticas(grupo$area_ha), "ha")
  mostrar_linha("Plantas", estatisticas(grupo$numero_plantas), "unid.")
  mostrar_linha("Insumo", estatisticas(grupo$quantidade_insumo_kg), "kg")
  resultados[[cultura_atual]] <- data.frame(
    cultura = cultura_atual,
    quantidade_talhoes = nrow(grupo),
    media_area_ha = mean(grupo$area_ha),
    desvio_area_ha = if (nrow(grupo) > 1) sd(grupo$area_ha) else NA_real_,
    media_insumo_kg = mean(grupo$quantidade_insumo_kg),
    desvio_insumo_kg = if (nrow(grupo) > 1) sd(grupo$quantidade_insumo_kg) else NA_real_
  )
}

pasta_saida <- file.path(diretorio_script, "saida_R")
dir.create(pasta_saida, showWarnings = FALSE)
consolidado <- do.call(rbind, resultados)
write.csv(
  consolidado,
  file.path(pasta_saida, "estatisticas_por_cultura.csv"),
  row.names = FALSE,
  fileEncoding = "UTF-8"
)

png(file.path(pasta_saida, "areas_por_talhao.png"), width = 1000, height = 650)
cores <- ifelse(dados$cultura == "Açaí", "#6A1B9A", "#2E7D32")
barplot(
  dados$area_ha,
  names.arg = dados$talhao,
  col = cores,
  las = 2,
  ylab = "Área (hectares)",
  main = "Área dos talhões - FarmTech Pará",
  border = NA
)
legend(
  "topright",
  legend = c("Açaí", "Mandioca"),
  fill = c("#6A1B9A", "#2E7D32"),
  border = NA
)
dev.off()

cat("\nArquivos gerados em:", normalizePath(pasta_saida), "\n")
cat("- estatisticas_por_cultura.csv\n- areas_por_talhao.png\n")
