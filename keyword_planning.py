# def map_locations_ids_to_resource_names(client, location_ids):
#     geo_target_constants_service = client.get_service("GeoTargetConstantService")
#     resource_names = []
#     for location_id in location_ids:
#         resource_name = geo_target_constants_service.geo_target_constant_path(location_id)
#         resource_names.append(resource_name)
#     return resource_names

# def main(client, customer_id, location_ids, language_id, keyword_texts=None, page_url=None):
#     keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
#     keyword_competition_level_enum = client.enums.KeywordPlanCompetitionLevelEnum
#     keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
#     location_rns = map_locations_ids_to_resource_names(client, location_ids)
#     language_rn = client.get_service("GoogleAdsService").language_constant_path(language_id)

#     if not (keyword_texts or page_url):
#         raise ValueError("At least one of keywords or page URL is required, but neither was specified.")

#     request = client.get_type("GenerateKeywordIdeasRequest")
#     request.customer_id = customer_id
#     request.language = language_rn
#     request.geo_target_constants = location_rns
#     request.include_adult_keywords = False
#     request.keyword_plan_network = keyword_plan_network

#     if not keyword_texts and page_url:
#         request.url_seed.url = page_url

#     if keyword_texts and not page_url:
#         request.keyword_seed.keywords.extend(keyword_texts)

#     if keyword_texts and page_url:
#         request.keyword_and_url_seed.url = page_url
#         request.keyword_and_url_seed.keywords.extend(keyword_texts)

#     keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(request=request)

#     for idea in keyword_ideas:
#         competition_value = idea.keyword_idea_metrics.competition.name
#         print(
#             f'Keyword idea text "{idea.text}" has '
#             f'"{idea.keyword_idea_metrics.avg_monthly_searches}" '
#             f'average monthly searches and "{competition_value}" '
#             "competition.\n"
#         )

# if __name__ == "__main__":
#     from google.ads.googleads.client import GoogleAdsClient

#     client = GoogleAdsClient.load_from_storage("google-ads.yaml")
#     customer_id = "4394606043"
#     location_ids = ["1014522"]  # E.g., ["1014522"] for Dallas
#     language_id = "1000"  # E.g., "1000" for English
#     keyword_texts = ["bakery", "bakeries", "cake shop"]  # Example keywords
#     page_url = None  # Optional: a URL related to bakeries

#     main(client, customer_id, location_ids, language_id, keyword_texts, page_url)









import csv

def map_locations_ids_to_resource_names(client, location_ids):
    geo_target_constants_service = client.get_service("GeoTargetConstantService")
    resource_names = []
    for location_id in location_ids:
        resource_name = geo_target_constants_service.geo_target_constant_path(location_id)
        resource_names.append(resource_name)
    return resource_names

def main(client, customer_id, location_ids, language_id, keyword_texts=None, page_url=None):
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
    keyword_competition_level_enum = client.enums.KeywordPlanCompetitionLevelEnum
    keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
    location_rns = map_locations_ids_to_resource_names(client, location_ids)
    language_rn = client.get_service("GoogleAdsService").language_constant_path(language_id)

    if not (keyword_texts or page_url):
        raise ValueError("At least one of keywords or page URL is required, but neither was specified.")

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = language_rn
    request.geo_target_constants = location_rns
    request.include_adult_keywords = False
    request.keyword_plan_network = keyword_plan_network

    if not keyword_texts and page_url:
        request.url_seed.url = page_url

    if keyword_texts and not page_url:
        request.keyword_seed.keywords.extend(keyword_texts)

    if keyword_texts and page_url:
        request.keyword_and_url_seed.url = page_url
        request.keyword_and_url_seed.keywords.extend(keyword_texts)

    keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(request=request)

    with open('keyword_ideas.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Keyword Text", "Average Monthly Searches", "Competition"])
        
        for idea in keyword_ideas:
            competition_value = idea.keyword_idea_metrics.competition.name
            writer.writerow([
                idea.text,
                idea.keyword_idea_metrics.avg_monthly_searches,
                competition_value
            ])
            print(
                f'Keyword idea text "{idea.text}" has '
                f'"{idea.keyword_idea_metrics.avg_monthly_searches}" '
                f'average monthly searches and "{competition_value}" '
                "competition.\n"
            )

if __name__ == "__main__":
    from google.ads.googleads.client import GoogleAdsClient

    client = GoogleAdsClient.load_from_storage("google-ads.yaml")
    customer_id = "4394606043"
    location_ids = ["1014522"]  # E.g., ["1014522"] for Dallas
    language_id = "1000"  # E.g., "1000" for English
    keyword_texts = ["bakery", "bakeries", "cake shop"]  # Example keywords
    page_url = None  # Optional: a URL related to bakeries

    main(client, customer_id, location_ids, language_id, keyword_texts, page_url)
