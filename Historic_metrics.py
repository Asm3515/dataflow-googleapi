import csv

def main(client, customer_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    generate_historical_metrics(client, customer_id)


def generate_historical_metrics(client, customer_id):
    """Generates historical metrics and prints the results.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    googleads_service = client.get_service("GoogleAdsService")
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
    request = client.get_type("GenerateKeywordHistoricalMetricsRequest")
    request.customer_id = customer_id
    request.keywords.extend(["bakery near me", "publix bakery", "cakes"])
    # Geo target constant 2840 is for USA.
    request.geo_target_constants.append(
        googleads_service.geo_target_constant_path("1014522")
    )
    request.keyword_plan_network = (
        client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
    )
    # Language criteria 1000 is for English. For the list of language criteria
    # IDs, see:
    # https://developers.google.com/google-ads/api/reference/data/codes-formats#languages
    request.language = googleads_service.language_constant_path("1000")

    response = keyword_plan_idea_service.generate_keyword_historical_metrics(
        request=request
    )

    with open('historical_metrics.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Search Query", "Close Variants", "Approx. Monthly Searches",
            "Competition Level", "Competition Index", "Top of Page Bid Low Range",
            "Top of Page Bid High Range", "Monthly Search Volumes"
        ])

        for result in response.results:
            metrics = result.keyword_metrics
            monthly_search_volumes = "; ".join(
                [f"{month.month.name} {month.year}: {month.monthly_searches}" for month in metrics.monthly_search_volumes]
            )
            writer.writerow([
                result.text,
                ", ".join(result.close_variants) if result.close_variants else 'None',
                metrics.avg_monthly_searches,
                metrics.competition.name,
                metrics.competition_index,
                metrics.low_top_of_page_bid_micros,
                metrics.high_top_of_page_bid_micros,
                monthly_search_volumes
            ])
            print(
                f"The search query '{result.text}' (and the following variants: "
                f"'{result.close_variants if result.close_variants else 'None'}'), "
                "generated the following historical metrics:\n"
            )

            print(f"\tApproximate monthly searches: {metrics.avg_monthly_searches}")
            print(f"\tCompetition level: {metrics.competition.name}")
            print(f"\tCompetition index: {metrics.competition_index}")
            print(f"\tTop of page bid low range: {metrics.low_top_of_page_bid_micros}")
            print(f"\tTop of page bid high range: {metrics.high_top_of_page_bid_micros}")

            for month in metrics.monthly_search_volumes:
                print(
                    f"\tApproximately {month.monthly_searches} searches in "
                    f"{month.month.name}, {month.year}"
                )


if __name__ == "__main__":
    from google.ads.googleads.client import GoogleAdsClient

    client = GoogleAdsClient.load_from_storage("google-ads.yaml")
    customer_id = "4394606043"
    main(client, customer_id)
