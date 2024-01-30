clear variables;

% Facteur d'échelle
facteur_echelle = 3;

lpdipole = lpda('BoardWidth', [117.96e-3 325e-3]); % Largeur de la carte

% Ajuster les paramètres pour une fréquence centrale autour de 800 MHz
lpdipole.BoardLength = 420.47e-3;  % Longueur de la carte
lpdipole.Height = 1.6e-3;  % Hauteur de l'antenne
lpdipole.StripLineWidth = 0.0035;  % Largeur de la bande centrale
lpdipole.FeedLength =0.001;  % Longueur du bras central avant les autres bras
lpdipole.ArmWidth = [0.001 0.00112 0.00125 0.00141 0.00158 0.00178 0.002 0.00224 0.00252 0.00283 0.00318 0.00357 0.00402 0.00451 0.00507 0.00570 0.00640]; % Largeur des bras
lpdipole.ArmSpacing = [0.00939 0.01054 0.01185 0.01331 0.01496 0.01681 0.01888 0.02123 0.02383 0.02679 0.03010 0.03381 0.038 0.04269 0.04797 0.0539]; % Espacement entre chaque bras
lpdipole.ArmLength = [0.03796 0.04266 0.04793 0.05385 0.06051 0.06799 0.07639 0.08583 0.09444 0.10836 0.12176 0.13680 0.15371 0.17271 0.19406 0.21805 0.245]*0.5; % Longueur des bras

% Afficher les propriétés de l'antenne
show(lpdipole)

freq = linspace(775e6, 825e6, 21);
figure;
impedance(lpdipole,freq)
figure;
pattern(lpdipole,800e6)