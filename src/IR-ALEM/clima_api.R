# FarmTech Solutions - consulta meteorológica pública para municípios do Pará
# API Open-Meteo: https://open-meteo.com/

if (!requireNamespace("jsonlite", quietly = TRUE)) {
  stop("Pacote 'jsonlite' ausente. Execute: Rscript instalar_pacotes.R")
}

municipios <- data.frame(
  nome = c("Belém", "Santarém", "Marabá", "Castanhal", "Altamira"),
  latitude = c(-1.4558, -2.4431, -5.3811, -1.2969, -3.2038),
  longitude = c(-48.4902, -54.7083, -49.1331, -47.9211, -52.2064),
  stringsAsFactors = FALSE
)

descricao_tempo <- function(codigo) {
  if (codigo == 0) return("céu limpo")
  if (codigo %in% c(1, 2, 3)) return("parcialmente nublado ou encoberto")
  if (codigo %in% c(45, 48)) return("neblina")
  if (codigo %in% 51:57) return("garoa")
  if (codigo %in% 61:67) return("chuva")
  if (codigo %in% 71:77) return("neve")
  if (codigo %in% 80:82) return("pancadas de chuva")
  if (codigo %in% 85:86) return("pancadas de neve")
  if (codigo %in% 95:99) return("trovoadas")
  "condição não classificada"
}

consultar_clima <- function(municipio) {
  base <- "https://api.open-meteo.com/v1/forecast"
  parametros <- paste0(
    "?latitude=", municipio$latitude,
    "&longitude=", municipio$longitude,
    "&current=temperature_2m,relative_humidity_2m,apparent_temperature,",
    "precipitation,weather_code,wind_speed_10m",
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum",
    "&timezone=America%2FBelem&forecast_days=7"
  )

  resposta <- tryCatch(
    jsonlite::fromJSON(paste0(base, parametros)),
    error = function(e) {
      message("Falha na consulta: ", conditionMessage(e))
      NULL
    }
  )
  if (is.null(resposta)) return(invisible(FALSE))

  atual <- resposta$current
  diario <- resposta$daily
  cat("\n============================================================\n")
  cat(" CLIMA EM", toupper(municipio$nome), "- PARÁ\n")
  cat("============================================================\n")
  cat("Atualização:", atual$time, "\n")
  cat(sprintf("Temperatura: %.1f °C | Sensação: %.1f °C\n", atual$temperature_2m, atual$apparent_temperature))
  cat(sprintf("Umidade: %.0f%% | Vento: %.1f km/h\n", atual$relative_humidity_2m, atual$wind_speed_10m))
  cat(sprintf("Precipitação atual: %.1f mm | Condição: %s\n", atual$precipitation, descricao_tempo(atual$weather_code)))
  cat("\nPREVISÃO PARA 7 DIAS\n")
  for (i in seq_along(diario$time)) {
    cat(sprintf(
      "%s | mín %.1f °C | máx %.1f °C | chuva %.1f mm\n",
      diario$time[i], diario$temperature_2m_min[i],
      diario$temperature_2m_max[i], diario$precipitation_sum[i]
    ))
  }
  invisible(TRUE)
}

# Lê a entrada corretamente tanto no console interativo do R/RStudio quanto
# quando o arquivo é iniciado com "Rscript clima_api.R". Nesse segundo caso,
# readline() pode retornar imediatamente uma string vazia em alguns terminais.
ler_entrada <- function(mensagem, conexao_terminal = NULL) {
  if (interactive()) {
    return(readline(mensagem))
  }

  cat(mensagem)
  flush.console()
  entrada <- readLines(con = conexao_terminal, n = 1, warn = FALSE)

  # O comprimento zero indica que a entrada padrão foi encerrada (EOF).
  # Retornar NULL permite finalizar o programa, evitando um loop infinito.
  if (length(entrada) == 0) return(NULL)

  trimws(entrada[[1]])
}

main <- function() {
  # Em Rscript, stdin() pode apontar para o arquivo que contém o próprio
  # script. file("stdin") abre a entrada padrão real do processo, isto é, o
  # teclado do terminal. A conexão permanece aberta durante todo o menu.
  conexao_terminal <- NULL
  if (!interactive()) {
    conexao_terminal <- file("stdin", open = "r")
    on.exit(close(conexao_terminal), add = TRUE)
  }

  repeat {
    cat("\n=== API METEOROLÓGICA - PARÁ ===\n")
    for (i in seq_len(nrow(municipios))) {
      cat(sprintf("%d - %s\n", i, municipios$nome[i]))
    }
    cat("0 - Sair\n")

    entrada <- ler_entrada("Escolha um município: ", conexao_terminal)
    if (is.null(entrada)) {
      cat("\nEntrada encerrada. Consulta finalizada.\n")
      break
    }

    opcao <- suppressWarnings(as.integer(entrada))
    if (!is.na(opcao) && opcao == 0) {
      cat("Consulta encerrada.\n")
      break
    } else if (!is.na(opcao) && opcao >= 1 && opcao <= nrow(municipios)) {
      consultar_clima(municipios[opcao, ])
    } else {
      cat("Opção inválida. Tente novamente.\n")
    }
  }
}

if (sys.nframe() == 0) main()
