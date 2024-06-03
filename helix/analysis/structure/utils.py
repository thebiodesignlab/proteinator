from Bio.PDB import NeighborSearch, PDBParser, PDBIO
import os
from io import StringIO


def get_residues_within_distance(structure, target_residue, distance):
    """
    Given a protein structure, return all residues within a given distance from a target residue or ligand.

    Parameters
    ----------
    structure : Bio.PDB.Structure.Structure
        The protein structure to search within.
    target_residue : Bio.PDB.Residue.Residue
        The target residue or ligand to measure distances from.
    distance : float
        The distance threshold to consider.

    Returns
    -------
    list of Bio.PDB.Residue.Residue
        A list of residues within the given distance from the target residue.
    """
    # Extract all atoms from the structure
    atoms = [atom for atom in structure.get_atoms()]

    # Create a NeighborSearch object
    neighbor_search = NeighborSearch(atoms)

    # Get the center of mass of the target residue
    target_atoms = list(target_residue.get_atoms())
    target_center = sum(
        atom.coord for atom in target_atoms) / len(target_atoms)

    # Find all atoms within the given distance from the target center
    nearby_atoms = neighbor_search.search(target_center, distance)

    # Extract unique residues from the nearby atoms
    nearby_residues = {atom.get_parent() for atom in nearby_atoms}

    return list(nearby_residues)


def get_residue_by_position(structure, chain_id, residue_id):
    """
    Retrieve a residue or ligand from the structure by its chain ID and residue ID.

    Parameters
    ----------
    structure : Bio.PDB.Structure.Structure
        The protein structure to search within.
    chain_id : str
        The chain identifier.
    residue_id : int
        The residue identifier.

    Returns
    -------
    Bio.PDB.Residue.Residue
        The residue or ligand at the specified position.
    """
    chain = structure[0][chain_id]
    residue = chain[residue_id]
    return residue


def parse_pdb_file(pdb_input):
    """
    Parse a PDB file or raw PDB string and return the structure object.

    Parameters
    ----------
    pdb_input : str
        The path to the PDB file or the raw PDB string.

    Returns
    -------
    Bio.PDB.Structure.Structure
        The parsed structure object.
    """
    parser = PDBParser()

    if os.path.isfile(pdb_input):
        structure = parser.get_structure("structure", pdb_input)
    else:
        pdb_io = StringIO(pdb_input)
        structure = parser.get_structure("structure", pdb_io)

    return structure


def fetch_pdb_structure(pdb_id: str):
    import requests
    """
    Fetch a PDB structure by its ID and return as a Biopython Structure object.

    Parameters:
    - pdb_id (str): The PDB ID to fetch.

    Returns:
    - Bio.PDB.Structure.Structure: The fetched structure as a Biopython object.
    """
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(
            f"Failed to download PDB {pdb_id}. HTTP Status Code: {response.status_code}")

    pdb_content = response.text
    pdb_io = StringIO(pdb_content)

    parser = PDBParser(QUIET=True)  # QUIET=True suppresses warnings
    structure = parser.get_structure(pdb_id, pdb_io)

    return structure


def pdb_to_string(structure):
    io = PDBIO()
    io.set_structure(structure)
    output = StringIO()
    io.save(output)
    return output.getvalue()

# Example usage:
# structure = parse_pdb_file("example.pdb")
# target_residue = get_residue_by_position(structure, 'A', 234)  # Chain A, Residue 234
# residues_within_5A = get_residues_within_distance(structure, target_residue, 5.0)
