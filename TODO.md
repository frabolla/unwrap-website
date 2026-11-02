# TODO

## Download dell'app dal sito
Decisione: **Opzione A — link diretto a GitHub Releases**. ✅ Fatto.
Repo dell'app: **frabolla/unwrap-macOS-release**. Release v1.0
pubblicata il 23/09/2026, asset `Unwrap.dmg`.

- [x] Pubblicare il binario (.dmg) come asset di una GitHub Release del
      repo `frabolla/unwrap-macOS-release` (release v1.0).
- [x] Collegare in `index.html` (IT ed EN) il pulsante "Scarica per
      Mac" a
      `https://github.com/frabolla/unwrap-macOS-release/releases/latest/download/Unwrap.dmg`
      (il link `latest` punta sempre automaticamente all'ultima
      versione, senza doverlo aggiornare a ogni nuova release — **a
      patto che l'asset si chiami sempre `Unwrap.dmg` in ogni
      release futura**, altrimenti il link non troverà il file).
- [x] Collegare il link "Note di rilascio" a
      `https://github.com/frabolla/unwrap-macOS-release/releases`.
- [x] Confermato: `Unwrap.dmg` della release v1.0 è firmato con
      Developer ID ("Francesco Tarini", team 7SRQ79789G) e notarizzato
      da Apple — verificato il 23/09/2026 con
      `spctl -a -vv -t install Unwrap.dmg` → `accepted, source=Notarized
      Developer ID`.

## Aggiornamenti automatici (Sparkle)
- [x] Integrare [Sparkle](https://sparkle-project.org) nell'app per
      permettere l'auto-update fuori dal Mac App Store.
- [x] Generare e pubblicare il feed appcast (XML) a ogni release.
- [x] Firmare gli update con la chiave EdDSA di Sparkle.
- [ ] Aggiungere il changelog alle voci dell'appcast.
- [ ] Pubblicare ogni build con un tag nuovo, senza sostituire il file di
      una release esistente: la sostituzione azzera il contatore dei download
      e invalida la firma delle voci già nell'appcast.

## Distribuzione via Homebrew
- [ ] Creare una formula Homebrew **cask** per Unwrap, così l'app si
      installa con `brew install --cask unwrap`.
- [ ] Sottomettere il cask a `homebrew-cask` (o mantenere un tap proprio,
      tipo `frabolla/homebrew-unwrap`, come primo passo più semplice).
- [ ] Tenere il cask aggiornato ad ogni nuova release (si può automatizzare
      con GitHub Actions).

## Mac App Store
- [ ] Completare la versione MAS (sandboxing, review Apple) e riattivare il
      pulsante "Disponibile su Mac App Store" sul sito, rimosso il
      23/09/2026 perché non ancora pronta.
