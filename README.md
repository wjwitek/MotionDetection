# Motion Detection

### Instalacja zależności:

```bash
pip3 install -r requirements.txt
```

### Użycie

Uruchomienie interfejsu

```bash
python gui.py
```



### Funkcje:

- Slider `sensitivity` - ustala czułość wykrywania
- Slider `area` - ustala minimalną powierzchnię prostokąta wykrywającego

- Slidery `X1 X2 Y1 Y2` - ustalają kadrowanie
- Przycisk `Debug/Normal` - Zmienia tryb z normalnego na debugowanie i w drugą stronę
- Przycisk `Set Reference Frame` - Ustala klatkę źródłową na aktualną
- Pole tekstowe - Można w nie wpisać źródło. Przykładowo (powinny działać wszystkie źródła obsługiwane przez `OpenCV`)
  - `0` - Używa kamery internetowej
  - `<ścieżka do pliku>` - Uruchomi filmik z podanej ścieżki
- Przycisk `Change Source` - Ustali źródło na podane w textboxie
