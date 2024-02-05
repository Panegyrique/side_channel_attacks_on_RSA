%%%%%%%%%%%%%%%%%%%%%%%%% Paramètres modifiables %%%%%%%%%%%%%%%%%%%%%%%%%%
keylength = 32;

start = 0;
stop = 4000;
algo = 'montgomery';
threshold = 0.5;

% % moy_noise = 100;
% % data_noise = load(['D:\\PFE\\Code\\MATLAB\\noise\\noise_mean_' ...
% %     num2str(moy_noise) '.mat']);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%%%%%%%%%%%%%%%% Appel des fonctions %%%%%%%%%%%%%%%%%%%%%%%%%%%
data_filtered = filter(start, stop, algo, threshold);
display_bits(start, stop, data_filtered, keylength)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Fonctions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function data_filtered = filter(start, stop, algo, threshold)
    % Initialiser mag_sup
    mag_sup = [];

    % Créer une nouvelle barre de progression
    h = waitbar(0, 'Progression : 0%');

    % Boucle sur les fichiers
    for i = start:stop
        % Ouvrir le fichier     
        fid = fopen(['D:\PFE\Code\MATLAB\data_raw_' algo ...
            '\data_raw_' num2str(i) '.dat'], 'r');

        % Lire les données du fichier
        data = fread(fid, [2, inf], 'float32');

        % Convertir les données complexes
        data = data(1,:) + 1i*data(2,:);

        % Fermer le fichier
        fclose(fid);

        % Calculer l'amplitude (magnitude)
        mag_temp = abs(data);

        % % % Créer un vecteur de temps
        % % Fs = 3.2e6; % Fréquence d'échantillonnage
        % % dt = 1/Fs; % Intervalle de temps
        % % t = 0:dt:(length(mag)*dt)-dt; % Vecteur de temps

        % % % Tronquer data_noise.avg_mag à la taille de mag
        % % % Bien qu'il y ait un trigger, les fichiers ne sont pas parfaitement égaux en taille
        % % if data_noise.t(end) > t(end)
        % %     data_noise.avg_mag = data_noise.avg_mag(1:length(mag));
        % %     data_noise.t = data_noise.t(1:length(t));
        % % else
        % %     mag = mag(1:length(data_noise.avg_mag));
        % %     t = t(1:length(data_noise.t));
        % % end
        % % 
        % % % Afficher uniquement les points de mag qui sont supérieurs à data_noise.avg_mag
        % % mag_temp = mag;
        % % mag_temp(mag <= data_noise.avg_mag) = NaN; % Remplacer les points inférieurs ou égaux par NaN
        % % 
        % % % Normaliser l'amplitude
        % % mag_temp = (mag_temp - min(mag_temp)) / (max(mag_temp) - min(mag_temp));

        % Ajouter à mag_sup
        if isempty(mag_sup)
            mag_sup = mag_temp;
        else
            % Tronquer à la taille la plus petite
            min_length = min(length(mag_sup), length(mag_temp));
            mag_sup = mag_sup(1:min_length);
            mag_temp = mag_temp(1:min_length);

            % Ajouter à mag_sup
            mag_sup(~isnan(mag_temp)) = mag_temp(~isnan(mag_temp));
        end

        % Mettre à jour la barre de progression
        waitbar((i+1-start) / (stop+1-start), h, ...
            ['Progression : ', num2str(round((i+1-start) / ...
            (stop+1-start) * 100)), '%']);
    end

    % Fermer la barre de progression
    close(h);

    % Créer un vecteur de temps
    Fs = 3.2e6; % Fréquence d'échantillonnage
    dt = 1/Fs; % Intervalle de temps
    t = 0:dt:(length(mag_sup)*dt)-dt; % Vecteur de temps
        
    % Supprimer toutes les valeurs inférieures au threshold
    mag_sup(mag_sup < threshold) = NaN;

    % Remplacer les valeurs NaN par le minimum
    mag_sup(isnan(mag_sup)) = min(mag_sup);

    % Normalisation des données
    mag_final = (mag_sup - min(mag_sup)) / (max(mag_sup) - min(mag_sup));

    % Créer une nouvelle figure
    figure;

    % Afficher l'amplitude normalisée du signal
    plot(t, mag_final);
    xlabel('Temps (s)');
    ylabel('Amplitude normalisée');
    title(['Données filtrées (' num2str(stop-start) ' fichiers)']);

    % Créer une structure pour renvoyer t et mag
    data_filtered.t = t;
    data_filtered.mag = mag_final;
end

function display_bits(start, stop, data, keylength)
    % Créer une nouvelle figure
    figure;

    % Créer un bouton à cocher
    h = uicontrol('Style', 'checkbox', 'String', 'Afficher les bits', ...
                  'Position', [20 20 200 20], 'Callback', @update_graph);

    % Afficher l'amplitude normalisée du signal
    plot(data.t, data.mag);
    xlabel('Temps (s)');
    ylabel('Amplitude');
    title(['Données filtrées (' num2str(stop-start) ' fichiers)']);

    % Stocker les handles des lignes rouges
    redlines = [];

    function update_graph(source, ~)
        % Callback pour le bouton à cocher
        if source.Value == 1
            % Si le bouton est coché, ajouter les lignes rouges
            hold on;
            % Calculer l'intervalle de temps pour diviser t(end)
            interval = data.t(end) / keylength;
            for i = 0:interval:max(data_mag.t)
                redlines(end+1) = line([i i], ylim, 'Color', 'r');
            end
            hold off;
        else
            % Si le bouton n'est pas coché, supprimer les lignes rouges et rafraîchir le graphique
            delete(redlines);
            redlines = [];
            refreshdata;
        end
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%