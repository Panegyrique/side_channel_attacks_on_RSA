%%%%%%%%%%%%%%%%%%%%%%%%%% Paramètres modifiable %%%%%%%%%%%%%%%%%%%%%%%%%%
sec = 2;
moy_noise = 100;
path_data_noise = 'D:\\PFE\\Code\\MATLAB\\noise\\noise_raw_%d.dat';
path_mean_save = ['D:\\PFE\\Code\\MATLAB\\noise\\' ...
    'noise_mean_' num2str(moy_noise) '.mat'];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Variables
Fs = 3.2e6; % Fréquence d'échantillonnage
dt = 1/Fs; % Intervalle de temps
num_points = round(sec/dt); % Nombre de points correspondant à 2 secondes
total_mag = zeros(moy_noise, num_points); % Tableau des amplitudes

% Créer une nouvelle barre de progression
h = waitbar(0, 'Progression : 0%');

% Boucle sur tous les fichiers
for i = 0:moy_noise
    % Ouvrir le fichier
    filename = sprintf(path_data_noise, i);
    fid = fopen(filename, 'r');

    % Lire les données du fichier
    data = fread(fid, [2, inf], 'float32');

    % Convertir les données complexes
    data = data(1,:) + 1i*data(2,:);

    % Fermer le fichier
    fclose(fid);

    % Tronquer les données à num_points
    data = data(1:min(num_points, length(data)));

    % Calculer l'amplitude (magnitude)
    mag = abs(data);

    % Stocker l'amplitude dans le tableau
    total_mag(i+1, 1:length(mag)) = mag;

    % Mettre à jour la barre de progression
    waitbar((i+1) / (moy_noise+1), h);

    % Mettre à jour la barre de progression
    waitbar((i+1) / (moy_noise+1), h, ['Progression : ', ...
        num2str(round((i+1) / (moy_noise+1) * 100)), '%']);
end

% Fermer la barre de progression
close(h);

% Calculer l'amplitude moyenne à chaque point de temps
avg_mag = mean(total_mag, 1);

% Créer un vecteur de temps
t = 0:dt:(length(avg_mag)*dt)-dt;

% Afficher l'amplitude moyenne du signal
figure;
plot(t, avg_mag);
xlabel('Temps (s)');
ylabel('Amplitude moyenne');
title(['Bruit moyen sur ' num2str(moy_noise) ' acquisitions']);

% Sauvegarder les variables t et avg_mag
save(path_mean_save, 't', 'avg_mag');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%