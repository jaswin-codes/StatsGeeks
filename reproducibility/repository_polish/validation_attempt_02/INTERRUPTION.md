# Preserved interruption
The second validator attempt stopped on a cp1252 decoding error while reading the
new UTF-8 notebook. The new validator was corrected to request UTF-8 explicitly.
No original scientific file or environment was modified. Later checks exposed a
similar build-time derivative issue; the full first package was archived before
rebuilding from the original notebook using UTF-8.
