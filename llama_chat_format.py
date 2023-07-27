BOS, EOS = "<s>", "</s>"
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = """\
En tant qu'assistant d'une responsable qualité, votre tâche consiste à identifier si les thèmes issus des catégories suivantes sont mentionnés dans les commentaires. Les catégories comprennent :
['Qualité des soins et du service', "Respect de l'intimité", "Sortie de l'établissement", 'Prise en charge médicale et paramédicale', 'Suivi post-hospitalisation', 'Fluidité et personnalisation du parcours patient', 'Gestion de la douleur et administration de médicaments', "Disponibilité et humanité des professionnels de santé", "Délai d'attente et rapidité de prise en charge", 'Qualité des repas et des collations', "Accueil et processus d'admission", 'Services de maternité et de pédiatrie', 'Niveau sonore de l'établissement', 'Température de la chambre', "Accès à la salle d'opération", 'Procédures administratives', 'Services de WiFi et de télévision', "Clarté de l'information et des explications fournies", 'Qualité des locaux et des chambres', "Gestion des frais supplémentaires et des dépassements d'honoraires", "Accessibilité de l'établissement"].
Pour chaque classification, vous devez indiquer si le commentaire reflète un avis positif ou négatif sur la catégorie concernée.
Si le commentaire ne fait pas référence à l'une des catégories énumérées, la classification sera considérée comme non applicable.
Vos réponses doivent être rédigées en français et présentées sous la forme d'un tableau TSV. Les colonnes du tableau seront les suivantes : ["Catégorie", "Avis : positif, négatif ou non applicable", "Justification de la classification"]. Les lignes du tableau contiennent les 20 catégories énumérées ci-dessus.
"""

def format_to_llama_chat_style(history) -> str:
    # history has the following structure:
    # - dialogs
    # --- instruction
    # --- response (None for the most recent dialog)
    prompt = ""
    for i, dialog in enumerate(history[:-1]):
      instruction, response = dialog[0], dialog[1]
      # prepend system instruction before first instruction
      if i == 0:
        instruction = f"{B_SYS}{DEFAULT_SYSTEM_PROMPT}{E_SYS}" + instruction
      else:
        # the tokenizer automatically adds a bos_token during encoding,
        # for this reason the bos_token is not added for the first instruction
        prompt += BOS
      prompt += f"{B_INST} {instruction.strip()} {E_INST} {response.strip()} " + EOS

    # new instruction from the user
    new_instruction = history[-1][0].strip()

    # the tokenizer automatically adds a bos_token during encoding,
    # for this reason the bos_token is not added for the first instruction
    if len(history) > 1:
      prompt += BOS
    else:
      # prepend system instruction before first instruction
      new_instruction = f"{B_SYS}{DEFAULT_SYSTEM_PROMPT}{E_SYS}" + new_instruction

    prompt += f"{B_INST} {new_instruction} {E_INST}"
    return prompt