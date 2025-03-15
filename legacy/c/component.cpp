#include "global.h"
#include "Component.h"
#include <cmath>

Component::Component(int D_){
  N = 0;
  D = D_;
  kappa0 = 1.0;
  nu0 = D+2;
  kappa = kappa0;
  nu = nu0;
  m0.zeros(D);
  m.zeros(D);
  S0.eye(D, D);
  S.eye(D, D);
  L0.eye(D, D);
  L.eye(D, D);
}


Component::Component(int D_, arma::mat XX){
  D = D_;

  reinitialise(XX);
}

void Component::reinitialise(arma::mat X){
  N = 0;
  kappa0 = 1.0;
  nu0 = D+2;
  kappa = kappa0;
  nu = nu0;
  m0.zeros(D);
  m.zeros(D);
  S0.eye(D, D);
  S.eye(D, D);
  L0.eye(D, D);
  L.eye(D, D);

  int n = X.n_rows;
  for(int i=0; i<n; i++){
    add_sample(X.row(i).t());
  }
}


arma::mat Component::get_S(){
  return S - kappa * m * m.t();
}

bool Component::is_empty(){
  return (N == 0);
}

void Component::add_sample(arma::vec x){
  kappa = kappa + 1;
  nu = nu + 1;
  m = ((kappa - 1) * m + x) / kappa;
  L = chol_update_arma(L, sqrt(kappa/(kappa - 1)) * (x - m), D);
  N = N + 1;
  S = S + x * x.t();
}

void Component::rm_sample(arma::vec x){
  L = chol_downdate(L, sqrt(kappa/(kappa - 1)) * (x - m), D);
  kappa = kappa - 1;
  nu = nu - 1;
  m = ((kappa + 1) * m - x) / kappa;
  N = N - 1;
  S = S - x * x.t();
}

double Component::marginal_loglik(){
  return loglik_marginal_NIW_fast(N, D, kappa, nu, L, kappa0, nu0, L0);
}

double Component::posterior_predictive(arma::vec x){
  arma::vec m_updated = m + (x - m) / (kappa + 1);
  arma::mat L_updated = chol_update_arma(L, sqrt((kappa + 1)/kappa) * (x - m_updated), D);
  return loglik_marginal_NIW_fast(1, D, kappa + 1, nu + 1, L_updated, kappa, nu, L);
}


void Component::update_IW_pars(){
  Sigma = riwishart(nu, get_S());
  mu = arma::conv_to<arma::vec>::from(rmvnorm_arma(1, m, 1.0/kappa * Sigma));
}

arma::mat Component::get_Sigma(){
  return Sigma;
}

arma::vec Component::get_mu(){
  return mu;
}

