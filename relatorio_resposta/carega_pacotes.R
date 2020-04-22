carrega.pacote<-function(pacotes){
  pacotes<-readLines(pacotes)
  carrega<-lapply(pacotes, function(pacote){
    if (!require(pacote,character.only=TRUE)){
      cat("Baixando pacote",pacote, "... \n" )
      install.packages(pacote,lib="/usr/lib/R/site-library")
      require(pacote,character.only=TRUE)
    }
    else{
      cat("Pacote",pacote,"carregado! \n")
    }
  })
}


#carrega.pacote("pacotes.txt")



#pacote<-"dfrtopics"

#if (!require(pacote,character.only=TRUE)){
#  cat("Baixando pacote",pacote, "... \n" )
#  devtools::install_github("agoldst/dfrtopics",lib="/usr/lib/R/site-library")
#  require(pacote,character.only=TRUE)
#  }else{
#  cat("Pacote",pacote,"carregado! \n")
#  }
