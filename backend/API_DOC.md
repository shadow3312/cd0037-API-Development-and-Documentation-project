# DOCUMENTATION API
Application Trivia, le jeu de quiz numéro 1.

#### Collection Categories
`GET '/categories'`
> Retourne une liste de catégories dans laquelle les clés sont les ids et les valeurs les catégories

- Paramètres de requête: aucun
- Retour: Un objet avec une clé nommée `categories`, qui contient un objet de type clé: valeur `id: category_string`.

**Exemple de réponse:**
 
```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/categories/<int:category_id>/questions`
> Retourne une liste de questions basées sur une catégorie donnée
- Paramètres de requête:
    - `category_id`: l'id de la catégorie
- Retour: Un objet avec les propriétés suivantes:
    - `success`: un booléen qui indique si l'enregistrement s'est bien passé ou non
    - `questions`: la liste des questions de la catégorie
    - `total_questions`: le nombre total de questions de la catégorie
    - `current_category`: la catégorie actuelle

**Exemple de réponse:**
```json
{
    "success": true,
    "questions": [
        {
            "answer": "Dakar",
            "category": 4,
            "difficulty": 2,
            "id": 1,
            "question": "Quelle est la capitale du Senegal",
        },
        {
            "answer": "Hollywood",
            "category": 6,
            "difficulty": 1,
            "id": 5,
            "question": "Quelle est la ville du Cinema ?",
        },
        
    ]
}
```

#### Collection Questions

`GET '/questions'`
> Retourne une liste de questions, contenant le nombre total de questions, la catégorie actuelle, et les catégories disponibles
- Paramètres de requête:
    - `page`: La page sur laquelle on veut récupérer les questions
- Retour: Un objet avec les clés: `categories`, qui contient un objet de type clé: valeur `id: category_string`, `current_category`, qui contient la catégorie actuelle, `questions`, qui contient la liste des questions disponibles et `total_questions`, qui contient le nombre total de questions.

**Exemple de réponse:**
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "1",
    "total_questions": 12,
    "questions": [
        {
            "answer": "Dakar",
            "category": 4,
            "difficulty": 2,
            "id": 1,
            "question": "Quelle est la capitale du Senegal",
        },
        {
            "answer": "Hollywood",
            "category": 6,
            "difficulty": 1,
            "id": 5,
            "question": "Quelle est la ville du Cinema ?",
        },
        
    ]
}
```

`POST '/questions'`
> Crée une nouvelle question
- Paramètres de requête: aucun
- Request body:
    - `question`: la question à enregistrer
    - `answer`: la réponse à la question
    - `difficulty`: la difficulté de la question
    - `category`: la catégorie de la question
- Retour: Un objet avec les propriétés suivantes:
    - `success`: un booléen qui indique si l'enregistrement s'est bien passé ou non
    - `created`: l'id de la question créee 

**Exemple de réponse:**
```json
{
    "success": true,
    "created": 3
}
```



`GET '/questions/search'`
> Retourne une liste de questions basées sur un texte donné correspondant au titre de la question
- Paramètres de requête:
    - `searchTerm`: le texte à rechercher
- Retour: Un objet avec les propriétés suivantes:
    - `success`: un booléen qui indique si la recherche s'est bien passée ou non
    - `questions`: la liste des questions de la catégorie
    - `total_questions`: le nombre total de questions de la catégorie
    - `current_category`: la catégorie actuelle

**Exemple de réponse:**
```json
{
    "success": true,
    "questions": [
        {
            "answer": "Dakar",
            "category": 4,
            "difficulty": 2,
            "id": 1,
            "question": "Quelle est la capitale du Senegal",
        },
        {
            "answer": "Hollywood",
            "category": 6,
            "difficulty": 1,
            "id": 5,
            "question": "Quelle est la ville du Cinema ?",
        },
        
    ],
    "total_questions": 2,
    "current_category": "1"
}
```

`DELETE '/questions/<int:question_id>'`
> Supprime une question en fonction de son id
- Paramètres de requête:
    - `question_id`: l'id de la question à supprimer
- Retour: Un objet avec les propriétés suivantes:
    - `success`: un booléen qui indique si la suppression s'est bien passée ou non
    - `deleted`: l'id de la question supprimée

**Exemple de réponse:**
```json
{
    "success": true,
    "deleted": 3
}
```

#### Collection Quizz

`POST '/quizzes'`
> Retourne une question aléatoire dans une catégorie donnée
- Request body:
    - `previous_questions`: la liste des questions déjà posées
    - `quiz_category`: la catégorie de la question à poser
- Retour: Un objet avec les propriétés suivantes:
    - `success`: un booléen qui indique si la requête s'est bien passé ou non
    - `question`: la question à poser

**Exemple de réponse:**
```json
{
    "success": true,
    "question": {
        "answer": "Dakar",
        "category": 4,
        "difficulty": 2,
        "id": 1,
        "question": "Quelle est la capitale du Senegal",
    },
}
```
