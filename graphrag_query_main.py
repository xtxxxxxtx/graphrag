from graphrag.cli.query import run_global_search
import argparse
import json
from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="query graphrag. ",
    )

    parser.add_argument(
        "--question_dir",
        default="../eval_result/questions.txt",
        type=str,
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="../eval_result",
    )
    parser.add_argument(
        "--root_dir",
        type=str,
        default="./ad0122",
    )
    parser.add_argument(
        "--community_level",
        type=int,
        default=4,
    )

    args = parser.parse_args()

    if args.question_dir:
        with open(args.question_dir, "r") as f:
            questions = [question.rstrip("\n") for question in f]
    else:
        questions = ["How do amyloid beta circadian patterns change with respect to age and amyloid pathology"]

    results = []
    for question in questions:
        response, context_data = run_global_search(config_filepath=None, data_dir=None, root_dir=Path(args.root_dir), query=question, community_level=args.community_level, response_type="Multiple Paragraphs", streaming=False)
        results.append({"response": response, "query": question})

    with open(f"{args.output_dir}/graphrag_{args.community_level}_result.json", "w") as f:
        json.dump(results, f, indent=2)



