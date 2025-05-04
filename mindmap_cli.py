import json

class Node:
    def __init__(self, text):
        self.text = text
        self.children = []

    def add_child(self, child_text):
        child = Node(child_text)
        self.children.append(child)
        return child

    def remove_child_at(self, index):
        if 0 <= index < len(self.children):
            removed = self.children.pop(index)
            return removed
        else:
            return None

    def to_dict(self):
        return {
            "text": self.text,
            "children": [child.to_dict() for child in self.children]
        }

    @staticmethod
    def from_dict(data):
        node = Node(data["text"])
        for child_data in data.get("children", []):
            node.children.append(Node.from_dict(child_data))
        return node

    def display(self, level=0):
        print("  " * level + "- " + self.text)
        for idx, child in enumerate(self.children):
            print("  " * (level + 1) + f"[{idx}]")
            child.display(level + 2)

class MindMap:
    def __init__(self, root_text):
        self.root = Node(root_text)

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self.root.to_dict(), f, indent=2)
        print(f"Carte mentale sauvegardée dans {filename}")

    @staticmethod
    def load(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        mindmap = MindMap(data["text"])
        mindmap.root = Node.from_dict(data)
        print(f"Carte mentale chargée depuis {filename}")
        return mindmap

    def get_node_by_path(self, path):
        """
        Récupère un nœud via un chemin sous forme de liste d'indices.
        Exemple : [0, 1] pour accéder au 2e enfant du 1er enfant de la racine.
        """
        node = self.root
        try:
            for idx in path:
                node = node.children[idx]
            return node
        except (IndexError, AttributeError):
            return None

    def get_parent_and_index(self, path):
        """
        Récupère le parent du nœud ciblé par path et l'indice du nœud à supprimer.
        """
        if not path:
            return None, None  # Pas de parent pour la racine
        parent_path = path[:-1]
        idx = path[-1]
        parent = self.get_node_by_path(parent_path)
        return parent, idx

def main():
    print("=== Outil CLI de carte mentale ===")
    mindmap = None

    while True:
        print("\nOptions :")
        print("1. Créer une nouvelle carte mentale")
        print("2. Charger une carte mentale")
        print("3. Ajouter une idée/sous-idée")
        print("4. Afficher la carte mentale")
        print("5. Sauvegarder la carte mentale")
        print("6. Supprimer une idée/sous-idée")
        print("7. Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            titre = input("Titre de la carte mentale : ")
            mindmap = MindMap(titre)
        elif choix == "2":
            fichier = input("Nom du fichier à charger : ")
            try:
                mindmap = MindMap.load(fichier)
            except Exception as e:
                print(f"Erreur lors du chargement : {e}")
        elif choix == "3":
            if not mindmap:
                print("Veuillez d'abord créer ou charger une carte mentale.")
                continue
            chemin = input("Chemin vers le nœud parent (ex: 0.1.2, vide pour racine) : ")
            noeud = mindmap.root
            if chemin:
                try:
                    indices = [int(i) for i in chemin.split(".")]
                    noeud = mindmap.get_node_by_path(indices)
                    if noeud is None:
                        print("Chemin invalide.")
                        continue
                except ValueError:
                    print("Chemin invalide.")
                    continue
            texte = input("Texte de la nouvelle carte : ")
            noeud.add_child(texte)
        elif choix == "4":
            if not mindmap:
                print("Aucune carte mentale chargée ou créée.")
            else:
                mindmap.root.display()
        elif choix == "5":
            if not mindmap:
                print("Aucune carte mentale à sauvegarder.")
            else:
                fichier = input("Nom du fichier de sauvegarde : ")
                try:
                    mindmap.save(fichier)
                except Exception as e:
                    print(f"Erreur lors de la sauvegarde : {e}")
        elif choix == "6":
            if not mindmap:
                print("Aucune carte mentale chargée ou créée.")
                continue
            chemin = input("Chemin vers l'idée à supprimer (ex: 0.1.2, vide interdit) : ")
            if not chemin:
                print("Vous ne pouvez pas supprimer la racine.")
                continue
            try:
                indices = [int(i) for i in chemin.split(".")]
            except ValueError:
                print("Chemin invalide.")
                continue
            parent, idx = mindmap.get_parent_and_index(indices)
            if parent is None:
                print("suppression invalide")
                continue
            removed = parent.remove_child_at(idx)
            if removed:
                print(f"Carte '{removed.text}' supprimée.")
            else:
                print("Chemin invalide")
        elif choix == "7":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()