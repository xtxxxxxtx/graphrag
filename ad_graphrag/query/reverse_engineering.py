import re
from graphrag.query.structured_search.global_search.search import GlobalSearchResult
def extract_id_from_response(text, type="Reports"):
    pattern = fr"{type}\s*\(([\d,\s\+more]*)\)"
    match = re.search(pattern, text)

    if match:
        # Extract the numbers and convert them into a list of integers
        report_ids = re.findall(r"\d+", match.group(1))
        return [str(id) for id in report_ids]
    else:
        return []


def from_answer_to_community(response, reports, print_communities=False):

    response_paragraphs = response.split("\n\n")

    refer_communities = {}
    for paragraph in response_paragraphs:
        communities = extract_id_from_response(paragraph)
        if len(communities) > 0:
            communities_df = reports.loc[reports["id"].isin(communities), :]
            refer_communities[paragraph] = communities_df

    if print_communities:
        for paragraph, communities_df in refer_communities.items():
            print("Response: " + paragraph + "\n" + "Reference communities: " + str(communities_df) + "\n\n")
            print("=" * 89)

    return refer_communities

def from_final_answer_to_communities(result, print_communities=True):
    response = result.response
    reports = result.context_data["reports"]
    return from_answer_to_community(response, reports, print_communities)

def from_map_response_to_communities_and_score(result, print_communities=True):
    map_responses = result.map_responses
    reports = result.context_data["reports"]
    all_refer_communities = []
    for map_response in map_responses:
        responses = map_response.response
        for response in responses:
            answer = response["answer"]
            score = response["score"]
            refer_communities = from_answer_to_community(answer, reports, False)
            all_refer_communities.append((refer_communities, score))
    if print_communities:
        for i, (refer_communities, score) in enumerate(all_refer_communities):
            print("="*30 + f"Map Response {i}: " + "=" * 30)
            for response, communities_df in refer_communities.items():
                print("Response: " + "\n" + response)
                print("Relevant Score: " + str(score))
                print("Reference Communities: " + str(communities_df) + "\n\n")

    return all_refer_communities


def from_community_to_entities(community_row, print_entities=True):
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





