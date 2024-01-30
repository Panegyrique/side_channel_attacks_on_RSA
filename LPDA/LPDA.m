% Design of a Log-Periodic Dipole Antenna (by Ramann Mantha)

% This design is based on the initial assumption that the directivity (D0)(ranging from 7dB-11.5dB in accordance with fig 11.13 in Balanis) and bandwith (fL and fH) are given
clc;
D0 = input('\nEnter the Value of Directivity = ');
fL = input('\nEnter the Lower cut-off frequency (in MHz) = ');
fH = input('\nEnter the Upper cut-off frequency (in MHz) = ');

if D0 == 7;
sigma = 0.135;
tau = 0.77;

elseif D0 == 7.5;
    sigma = 0.145;
    tau = 0.83;

elseif D0 == 8;
    sigma = 0.157;
    tau = 0.865;

elseif D0 == 8.5;
    sigma = 0.17;
    tau = 0.90;

elseif D0 == 9;
    sigma = 0.172;
    tau = 0.93;

elseif D0 == 9.5;
    sigma = 0.178;
    tau = 0.945;

elseif D0 == 10;
    sigma = 0.18;
    tau = 0.957;

elseif D0 == 10.5;
    sigma = 0.182;
    tau = 0.97;

elseif D0 == 11;
    sigma = 0.19;
    tau = 0.975;
end

fprintf('\nsigma = %f\n\n', sigma);
fprintf('tau = %f\n\n', tau);
alpha = atand((1-tau)/(4*sigma));
fprintf('alpha = %f\n\n', alpha);

% Bandwidth of active region is denoted by "Bactreg" and slightly higher
% bandwidth is denoted by "Bs"
Bactreg = 1.1+7.7*((1-tau)^2)*cotd(alpha);
fprintf('Bactreg = %f\n\n', Bactreg);
Bs = (fH/fL)*Bactreg;
fprintf('Bs = %f\n\n', Bs);

% Number of elements is denoted by N
ln = @log;
intermediate1 = 1+(ln(Bs)/ln(1/tau));
N = ceil(intermediate1);
fprintf('N = %f\n\n', N);

f1 = 2/((Bs/fH)+(1/fL));
f2 = fH*(2-(f1/fL));
fprintf('f1 = %f\n\n', f1);
fprintf('f2 = %f\n\n', f2);

c = 300;
lambda_max = c/f1;
fprintf('lambda_max = %f\n\n', lambda_max);
L = (lambda_max/4)*(1-(1/Bs))*cotd(alpha);
fprintf('L = %f\n\n', L);
l_max = lambda_max/2;
fprintf('l_max = %f\n\n', l_max);

for i = 1:1:N-1;
    intermediate2 = ((tau)^(i-1))*(l_max);
    l_i = (tau)*intermediate2;
    fprintf('l_i = %f\n', l_i);
end

R_max = l_max/(2*tand(alpha));
fprintf('\nR_max = %f\n\n', R_max);

for j = 1:1:N-1;
    intermediate3 = ((tau)^(j-1))*(R_max);
    R_j = (tau)*intermediate3;
    fprintf('R_j = %f\n', R_j);
end

L_actual = R_max - R_j;
fprintf('\nL_actual = %f\n\n', L_actual);

spacing_factor = ((R_max)-((R_max)*(tau)))/(2*(l_max));
fprintf('spacing_factor = %f\n\n', spacing_factor);