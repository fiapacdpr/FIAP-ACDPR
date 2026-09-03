pacotes <- c("jsonlite")
ausentes <- pacotes[!vapply(pacotes, requireNamespace, logical(1), quietly = TRUE)]

if (length(ausentes) == 0) {
  cat("Todos os pacotes necessários já estão instalados.\n")
} else {
  cat("Instalando:", paste(ausentes, collapse = ", "), "\n")
  install.packages(ausentes, repos = "https://cloud.r-project.org")
}
