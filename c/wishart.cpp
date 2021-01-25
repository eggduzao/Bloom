#include "global.h"

arma::mat rwishart(unsigned int df, const arma::mat& S){

  unsigned int m = S.n_rows;

  arma::mat Z(m,m);

  for(unsigned int i = 0; i < m; i++){
    Z(i,i) = sqrt(R::rchisq(df-i));
  }

  for(unsigned int j = 0; j < m; j++){
    for(unsigned int i = j+1; i < m; i++){
      Z(i,j) = R::rnorm(0,1);
    }
  }

  arma::mat C = arma::trimatl(Z).t() * arma::chol(S);

  return C.t()*C;
}

arma::mat riwishart(unsigned int df, const arma::mat& S){
  return rwishart(df,S.i()).i();
}

arma::mat rmvnorm_arma(int n, arma::vec mu, arma::mat sigma) {
  int ncols = sigma.n_cols;
  arma::mat Y = arma::randn(n, ncols);
  return arma::repmat(mu, 1, n).t() + Y * arma::chol(sigma);
}

const double log2pi = std::log(2.0 * M_PI);

arma::vec dmvnrm_arma(arma::mat x, arma::rowvec mean, arma::mat sigma, bool logd = false) {
  int n = x.n_rows;
  int xdim = x.n_cols;
  arma::vec out(n);
  arma::mat rooti = arma::trans(arma::inv(trimatu(arma::chol(sigma))));
  double rootisum = arma::sum(log(rooti.diag()));
  double constants = -(static_cast<double>(xdim)/2.0) * log2pi;

  for (int i=0; i < n; i++) {
    arma::vec z = rooti * arma::trans( x.row(i) - mean) ;
    out(i)      = constants - 0.5 * arma::sum(z%z) + rootisum;
  }

  if (logd == false) {
    out = exp(out);
  }
  return(out);
}

