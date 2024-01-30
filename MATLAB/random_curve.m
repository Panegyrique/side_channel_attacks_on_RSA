% Algorithme utilisé
algo = 'square_and_multiply';

% Nombre total de fichiers
total_files = 3000;

% Nombre de fichiers à sélectionner
num_files = 5;

% Sélectionner aléatoirement num_files fichiers parmi total_files
selected_files = randperm(total_files, num_files);

% Boucle sur les fichiers sélectionnés
for i = 1:num_files
    % Ouvrir le fichier
    filename = sprintf('D:\\PFE\\Code\\MATLAB\\data_raw_%s\\data_raw_%d.dat', algo, selected_files(i));
    fid = fopen(filename, 'r');

    % Lire les données du fichier
    data = fread(fid, [2, inf], 'float32');

    % Convertir les données en nombres complexes
    data = data(1,:) + 1i*data(2,:);

    % Fermer le fichier
    fclose(fid);

    % Calculer l'amplitude (magnitude)
    mag = abs(data);

    % Créer un vecteur de temps
    Fs = 3.2e6; % Fréquence d'échantillonnage
    dt = 1/Fs; % Intervalle de temps
    t = 0:dt:(length(mag)*dt)-dt; % Vecteur de temps

    % Créer une nouvelle figure
    figure;

    % Afficher l'amplitude normalisée du signal
    plot(t, mag);
    xlabel('Temps (s)');
    ylabel('Amplitude');
    title(sprintf('Amplitude du fichier %d', selected_files(i)));
end