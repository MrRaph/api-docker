# api-docker-service-ips

Ceci est un micro service écrit en Python avec [Flask](http://flask.pocoo.org/) et [Flask API](http://www.flaskapi.org/) fournissant une API permettant de récupérer les IP affectées par Docker à un service donné.

Lorsqu'un service est créé dans un cluster Docker utilisant le Swarm Mode, chaque container du-dit service dispose d'une IP qui lui est propre. Ceci ne change pas par rapport à la création classique d'un container. La nouveauté c'est que le Swarm Mode ajoute une vIP et un load balancer en amont de ces containers.

Les adresses IP générées ne sont pas simples à récupérer et ça se complique encore lorsque l'on souhaite les utiliser dans un script ou un micro service. C'est pourquoi j'ai créé ce petit micro service ! :)

# Fonctionnement

Ce micro service utilise la librairie [dnspython](http://www.dnspython.org/) pour résoudre de manière inverse les noms DNS créés par le Swarm Mode et attachés au service et à ses containers.

Le micro service retourne un object JSON contenant les correspondances en utilisant la forme suivante.

    {
      'service': name,
      'ip': addresses,
      'tasks': tasks,
      'error': ''
    }

`name` est le nom du service étudié, `addresses` est un tableau contenant les vIPs du service et `tasks` est un tableau contenant les IPs des containers. `error` contient une valeur non vide que quand quelque chose de passe mal.

# Utilisation

Tout d'abord, voyons comment récupérer ce micro service.

## Installation

Pour utiliser cet outil, vous avez deux possibilité, soit de le construire depuis les sources - `docker build ...` - soit de récupérer directement l'image construite depuis le dépôt Git.

### Build manuel

Afin de construire l'image par vous même, vous devrez dans un premier temps, clone le dépôt Git.

    git clone https://github.com/MrRaph/api-docker-service-ips.git

Puis lancer la construction de l'image Docker

    cd api-docker-service-ips
    docker build -t api-docker-service-ips .

### Utilisation de l'image Docker

Pour utiliser directement l'image Docker éxistant dans le repo, rien de plus simple, il suffit d'utiliser la commande ci-dessous.

    docker pull mrraph/api-docker-service-ips

## Création du service

Maintenant que vous disposez de l'image dans votre infrastructure, il faut créer un service avec. Pour cela, voici la commande à utiliser.

    docker service create --replicas 1 --network web \
    --restart-condition any --name api-docker-service-ips \
    mrraph/api-docker-service-ips

Ceci va créer un service avec un seul container dans votre cluster Swarm, vous pouvez bien entendu ajouter plus de container en changeant la valeur sur paramètre `--replicas` ou en utilisant la commande `docker service scale api-docker-service-ips=<nombre de containers souhaité>`

# Récupérer les IPs avec l'outil

Rentrons maintenant dans le vif du sujet, voici comment utiliser l'outil api-docker-service-ips pour récupérer les ips d'un service.

### Récupérer la vIP d'un service

Pour récupérer la vIP d'un service, l'outil api-docker-service-ips expose une URL de la forme : [http://127.0.0.1:5000/docker/service/<service_name>/ip](http://127.0.0.1:5000/docker/service/<service_name>/ip)

Voici un exemple d'utilisation pour récupérer la vIP du service `api-docker-service-ips` :

    curl -X GET http://api-docker-service-ips:5000/docker/service/api-docker-service-ips/ip
    {"ip": ["10.0.0.9"], "tasks": ["10.0.0.19"], "service": "api-docker-service-ips", "error": ""}

### Récupérer les IP des containers d'un service

Pour récupérer les IP des containers d'un service, l'outil api-docker-service-ips expose une URL de la forme : [http://127.0.0.1:5000:5000/docker/service/<service_name>/tasks/ip](http://127.0.0.1:5000/docker/service/<service_name>/tasks/ip)

Voici un exemple d'utilisation pour récupérer les IP des containers du service `api-docker-service-ips` :

    curl -X GET http://api-docker-service-ips:5000/docker/service/api-docker-service-ips/tasks/ip
    {"tasks": ["10.0.0.19"], "service": "api-docker-service-ips", "error": ""}
