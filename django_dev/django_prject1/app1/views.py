from django.shortcuts import render
from django.http import HttpResponse
import statistics
# Vue pour la page de traitement de fichier
def index(request):
    return render(request, 'app1/index.html')

# Vue pour effectuer les calculs statistiques
def calcules(request):
    mean = None
    median = None
    mode = None
    variance = None
    stdev = None
    calcul_type = request.GET.get('type')  # Récupérer le paramètre 'type' passé dans l'URL

    if request.method == 'POST':
        # Récupération des valeurs envoyées par le formulaire
        valeurs = request.POST.get('valeurs')

        if valeurs:
            # Conversion de la chaîne de valeurs en une liste de nombres
            try:
                # On remplace les virgules par des tirets pour uniformiser la séparation
                valeurs = [float(val) for val in valeurs.replace(',', '-').split('-')]

                # Vérification du type de calcul à effectuer
                if calcul_type == 'moyenne':
                    mean = statistics.mean(valeurs)
                elif calcul_type == 'mediane':
                    # On calcule la médiane, qui est la valeur du milieu après tri
                    valeurs_triees = sorted(valeurs)
                    median = statistics.median(valeurs_triees)
                elif calcul_type == 'mode':
                    # Le mode peut avoir plusieurs valeurs, donc on gère les exceptions
                    try:
                        mode = statistics.mode(valeurs)
                    except statistics.StatisticsError:
                        mode = "Plusieurs modes ou pas de mode"
                elif calcul_type == 'total':
                    # Calcul complet : Moyenne, Médiane, Mode, Variance, Ecart-type
                    mean = statistics.mean(valeurs)
                    # On calcule la médiane
                    valeurs_triees = sorted(valeurs)
                    median = statistics.median(valeurs_triees)
                    try:
                        mode = statistics.mode(valeurs)
                    except statistics.StatisticsError:
                        mode = "Plusieurs modes ou pas de mode"
                    # On calcule la variance et l'écart-type
                    variance = statistics.variance(valeurs)
                    stdev = statistics.stdev(valeurs)
                else:
                    return HttpResponse("Erreur : Type de calcul inconnu.")

            except ValueError:
                return HttpResponse("Erreur : Assurez-vous d'entrer uniquement des nombres valides.")
            except statistics.StatisticsError as e:
                return HttpResponse(f"Erreur statistique : {e}")

    return render(request, 'app1/calcules.html', {
        'mean': mean,
        'median': median,
        'mode': mode,
        'calcul_type': calcul_type,  # Passer le type de calcul à la page de résultats
        'form': request.POST  # Pour préremplir le formulaire avec les valeurs soumises
    })
