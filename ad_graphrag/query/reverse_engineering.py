import re
from graphrag.query.structured_search.global_search.search import GlobalSearchResult
import pandas as pd
from itertools import chain

def global_search_reverse_engineering(
        result,
        reverse_target="map_response",
        reverse_level="instance",
        entities=None,
        relationships=None,
        text_units=None,
        covariates=None):
    all_reference_infor = {}
    reports = result.context_data["reports"]

    # Community level reverse engineering.
    if reverse_target == "map_response":
        map_responses = result.map_responses
        for map_response in map_responses:
            responses = map_response.response
            for response in responses:
                infor = {}
                answer = response["answer"]
                score = response["score"]
                infor["score"] = score
                refer_communities = from_answer_to_community(answer, reports)
                infor["communities"] = refer_communities
                all_reference_infor[answer] = infor

    elif reverse_target == "reduced_response":
        response = result.response
        response_paragraphs = response.split("\n\n")
        for paragraph in response_paragraphs:
            infor = {}
            refer_communities = from_answer_to_community(paragraph, reports)
            infor["communities"] = refer_communities
            all_reference_infor[paragraph] = infor

    else:
        raise ValueError(f"The reverse target {reverse_target} is wrong.")

    if reverse_level == "community":
        return all_reference_infor

    # Instance level reverse engineering.
    if entities is not None:
        all_reference_infor = from_community_to_entities(all_reference_infor, entities, False)

    if relationships is not None:
        all_reference_infor = from_community_to_relationships(all_reference_infor, relationships, False)

    if covariates is not None:
        all_reference_infor = from_community_to_covariates(all_reference_infor, covariates, False)

    if reverse_level == "instance":
        return all_reference_infor

    all_reference_infor = from_entities_to_text_units(all_reference_infor, text_units, print_units=False)

    return all_reference_infor


def reverse_result_print(all_reference_infor, reverse_target="map_response"):
    if reverse_target == "map_response":
        response_type = "Map Response"
    elif reverse_target == "reduced_response":
        response_type = "Final Response"
    else:
        raise ValueError(f"The reverse target {reverse_target} is wrong.")

    for i, (response, infor) in enumerate(all_reference_infor.items()):
        print("=" * 30 + response_type + f" {str(i + 1)}" + "=" * 30)
        print("Response: " + response + "\n\n")
        if "score" in infor:
            print("Response relevant score from LLM: " + str(infor["score"]) + "\n\n")

        if "communities" in infor:
            print("Reference Communities: " + "\n" + str(infor["communities"]) + "\n\n")

        if "entities" in infor:
            print("Reference Entities: " + "\n" + str(infor["entities"]) + "\n\n")

        if "relationships" in infor:
            print("Reference Relationships: " + "\n" + str(infor["relationships"]) + "\n\n")

        if "covariates" in infor:
            print("Reference Covariates: " + "\n" + str(infor["covariates"]) + "\n\n")

        # if "text_units" in infor:
        #     print("Reference text units: \n")
        #     for text_unit in infor["text_units"]:
        #         print(text_unit)
        #         print("\n\n")
        #         print("*" * 120)

    return


def extract_id_from_response(text, type="Reports"):
    pattern = fr"{type}\s*\(([\d,\s\+more]*)\)"
    match = re.search(pattern, text)

    if match:
        # Extract the numbers and convert them into a list of integers
        report_ids = re.findall(r"\d+", match.group(1))
        return [str(id) for id in report_ids]
    else:
        return []


def from_answer_to_community(response, reports):

    communities = extract_id_from_response(response)
    if len(communities) > 0:
        return reports.loc[reports["id"].isin(communities), :]
    else:
        return None


def from_community_to_entities(all_reference_infor, entities, print_entities=True):
    for response in all_reference_infor.keys():
        infor = all_reference_infor[response]
        communities = infor["communities"]
        if communities is None:
            return
        all_communities_id = set(communities["id"].tolist())
        entities_df = {"title": [],
                       "description": [],
                       "type": [],
                       "id": [],
                       "short_id": [],
                       "community_ids": [],
                       "text_unit_ids": []}
        for e in entities:
            e_communities = set(e.community_ids)
            if len(all_communities_id.intersection(e_communities)) > 0:
                entities_df["id"].append(e.id)
                entities_df["short_id"].append(e.short_id)
                entities_df["title"].append(e.title)
                entities_df["type"].append(e.type)
                entities_df["description"].append(e.description)
                entities_df["community_ids"].append(e.community_ids)
                entities_df["text_unit_ids"].append(e.text_unit_ids)
        infor["entities"] = pd.DataFrame(entities_df)

    if print_entities:
        for i, reference_infor in enumerate(all_reference_infor):
            print("=" * 30 + f"Map Response {i}: " + "=" * 30)
            for response, infor in reference_infor.items():
                print("Response: " + "\n" + response)
                print("Reference entities: " + str(infor["entities"]) + "\n\n")

    return all_reference_infor

def from_community_to_relationships(all_reference_infor, relationships, print_rel=True):
    for response in all_reference_infor.keys():
        infor = all_reference_infor[response]
        all_entities = infor["entities"]["title"].tolist()
        relationships_df = {"description": [],
                       "source": [],
                       "target": [],
                       "weight": [],
                       "id": [],
                       "short_id": [],
                       "text_unit_ids": []}
        for r in relationships:
            source, target = r.source, r.target
            if source in all_entities or target in all_entities:
                relationships_df["id"].append(r.id)
                relationships_df["short_id"].append(r.short_id)
                relationships_df["description"].append(r.description)
                relationships_df["text_unit_ids"].append(r.text_unit_ids)
                relationships_df["source"].append(source)
                relationships_df["target"].append(target)
                relationships_df["weight"].append(r.weight)

        infor["relationships"] = pd.DataFrame(relationships_df)

    if print_rel:
        for i, reference_infor in enumerate(all_reference_infor):
            print("=" * 30 + f"Map Response {i}: " + "=" * 30)
            for response, infor in reference_infor.items():
                print("Response: " + "\n" + response)
                print("Reference Relationships: " + str(infor["rlationships"]) + "\n\n")

    return all_reference_infor


def from_entities_to_text_units(all_reference_infor, text_units, print_units=True):
    for response in all_reference_infor.keys():
        infor = all_reference_infor[response]
        all_text_units_ids = []
        if "entities" in infor:
            all_text_units_ids.extend(infor["entities"]["text_unit_ids"].tolist())
        if "relationships" in infor:
            all_text_units_ids.extend(infor["relationships"]["text_unit_ids"].tolist())

        all_text_units_ids = list(chain.from_iterable(all_text_units_ids))
        print(len(all_text_units_ids))
        all_text_units_ids = set(all_text_units_ids)
        all_text_units = [text_units[id] for id in all_text_units_ids]
        infor["text_units"] = all_text_units

    if print_units:
        for i, reference_infor in enumerate(all_reference_infor):
            print("=" * 30 + f"Map Response {i}: " + "=" * 30)
            for response, infor in reference_infor.items():
                print("Response: " + "\n" + response)
                print("Reference text units: " + "\n\n")
                for text_unit in infor["text_units"]:
                    print(text_unit)
                    print("\n\n")

    return all_reference_infor

def from_community_to_covariates(all_reference_infor, covariates, print_covariates=True):
    pass


if __name__ == "__main__":
    import pandas as pd
    response = "## Major Conflict\n\nThe central conflict in the story revolves around the Paranormal Military Squad's mission to establish contact with extraterrestrial intelligence. This undertaking is fraught with high-stakes operations and secrecy, highlighting the potential implications of first contact with alien beings. The team faces significant challenges, particularly in deciphering alien signals and managing the inherent risks associated with their mission. The tension between the desire for communication and the unknown nature of the extraterrestrial entities creates a compelling narrative conflict [Data: Reports (4, 5, 2, 3, 0)].\n\n## Protagonists\n\nThe protagonists of the story are key members of the Paranormal Military Squad, including Taylor Cruz, Dr. Jordan Hayes, Alex Mercer, and Sam Rivera. These characters are actively engaged in the mission to communicate with extraterrestrial intelligence, each contributing their unique skills and perspectives to the team's efforts [Data: Reports (4, 5, 3)].\n\n## Antagonist\n\nWhile the antagonist is not explicitly defined in the provided data, it can be inferred that the unknown nature of the extraterrestrial entities poses a significant challenge to the squad's objectives. The ambiguity surrounding these entities may represent an antagonistic force, complicating the team's mission and heightening the stakes of their endeavor [Data: Reports (4, 5, 3)].\n\nIn summary, the story's conflict centers on the Paranormal Military Squad's efforts to communicate with extraterrestrial intelligence, with the protagonists being the squad members and the antagonistic force represented by the unknown challenges posed by the extraterrestrial entities."
    contexts = {
        "id" : ["4", "5", "2", "3", "0"],
        "title": ["Dulce Base and the Paranormal Military Squad", "Sam Rivera and the Paranormal Military Squad a",
                  "Dulce Base: Extraterrestrial Research and Comm", "Operation: Dulce and the Paranormal Military S", "Dulce Base and the Paranormal Military Squad Team"],
        "occurrence weight": [1.0, 1.0, 0.75, 0.58, 0.41],
        "content": ["Dulce Base and the Paranormal Military Squad", "Sam Rivera and the Paranormal Military Squad a",
                  "Dulce Base: Extraterrestrial Research and Comm", "Operation: Dulce and the Paranormal Military S", "Dulce Base and the Paranormal Military Squad Team"],
        "rank": [8.5, 7.5, 8.5, 8.5, 8.5],
    }
    reports = pd.DataFrame(contexts)
    results = GlobalSearchResult(response=response, context_data={"reports": reports}, context_text="", completion_time=1, llm_calls=2, map_responses=" ", prompt_tokens=1, reduce_context_data=None, reduce_context_text=None)
    from_answer_to_community(results, None, True)





