from DrissionPage import ChromiumPage, ChromiumOptions
import time
import os
import json


def alibaba_image_search(image_path: str):
    # 1. Setup Session
    co = ChromiumOptions()
    co.set_user_data_path(r"C:\Users\vinay\Downloads\Alibaba_UserProfile")
    page = ChromiumPage(co)

    # 2. Navigate to Alibaba
    print("Opening Alibaba.com...")
    page.get("https://www.alibaba.com")
    time.sleep(5)

    try:
        # 3. Find and Click Image Search
        image_search_btn = page.ele("@data-search=switch-image-upload", timeout=10)
        if not image_search_btn:
            image_search_btn = page.ele(
                ".header-tab-switch-image-upload-multi", timeout=10
            )

        if image_search_btn:
            image_search_btn.click()
            time.sleep(3)

            # 4. Upload File
            if not os.path.exists(image_path):
                print(f"ERROR: Image not found at {image_path}")
                return

            file_input = page.ele(".upload-file", timeout=10)
            if not file_input:
                file_input = page.ele("@name=image-search-upload", timeout=10)

            if file_input:
                file_input.input(image_path)
                print("Image uploaded successfully! Waiting for results...")

                # Wait for results to load
                page.wait.url_change("/search/page?", timeout=30)

                # 5. Click "Suppliers" Tab
                suppliers_tab = page.ele("@dot-params:area=suppliers", timeout=10)
                if not suppliers_tab:
                    suppliers_tab = page.ele("text:Suppliers", timeout=10)

                if suppliers_tab:
                    suppliers_tab.click()
                    print("Navigated to Suppliers tab. Waiting for content...")
                    time.sleep(5)

                    # --- TARGETING THE SPECIFIC SECTION ---
                    # Only look for the exact <section class="content"> container
                    # then only collect cards with class "wYFEM REIxN" inside it.
                    try:
                        content_container = page.ele(
                            "tag:section@class=content", timeout=10
                        )
                    except Exception:
                        content_container = None

                    supplier_cards = []
                    if content_container:
                        try:
                            # select elements that have both classes wYFEM and REIxN
                            supplier_cards = page.eles("@class:wYFEM REIxN") or []
                        except Exception:
                            supplier_cards = []

                    print(
                        f"Found {len(supplier_cards)} supplier cards in the main content section."
                    )

                    if supplier_cards:
                        all_data = []

                        for card in supplier_cards:
                            try:
                                # Extract basic info
                                company_name = (
                                    card.ele(".iedPc").text
                                    if card.ele(".iedPc")
                                    else (card.ele("h2").text if card.ele("h2") else "")
                                )
                                location = (
                                    card.ele(".qoCWI").text
                                    if card.ele(".qoCWI")
                                    else ""
                                )
                                # Only accept gold years if the element (or the card) has
                                # data-supplier-card-gold-years="true" attribute.
                                gold_years = "N/A"
                                try:
                                    gy_elem = None
                                    try:
                                        gy_elem = card.ele('[data-supplier-card-gold-years="true"] .WDsPi')
                                    except Exception:
                                        gy_elem = None

                                    if not gy_elem:
                                        # fallback to any .WDsPi element if present
                                        gy_elem = card.ele('.WDsPi')

                                    if gy_elem:
                                        attr_val = None
                                        # try attribute on the found element
                                        try:
                                            attr_val = gy_elem.attr('data-supplier-card-gold-years')
                                        except Exception:
                                            try:
                                                attr_val = gy_elem.get_attribute('data-supplier-card-gold-years')
                                            except Exception:
                                                attr_val = None

                                        # if not present on element, check the card container
                                        if not attr_val:
                                            try:
                                                attr_val = card.attr('data-supplier-card-gold-years')
                                            except Exception:
                                                try:
                                                    attr_val = card.get_attribute('data-supplier-card-gold-years')
                                                except Exception:
                                                    attr_val = None

                                        if attr_val == "true":
                                            try:
                                                gold_years = gy_elem.text or "N/A"
                                            except Exception:
                                                gold_years = "N/A"
                                        else:
                                            gold_years = "N/A"
                                except Exception:
                                    gold_years = "N/A"
                                rating = (
                                    card.ele(".Y5RD3").text
                                    if card.ele(".Y5RD3")
                                    else "N/A"
                                )
                                reviews = (
                                    card.ele(".x4t8m").text
                                    if card.ele(".x4t8m")
                                    else "0"
                                )

                                # Extract Performance Metrics
                                metrics = {}
                                metric_items = card.eles(".DuZLU") or []
                                for item in metric_items:
                                    try:
                                        label = item.ele(".VwglV").text
                                        value = item.ele(".WgQ0R").text
                                        metrics[label] = value
                                    except Exception:
                                        continue

                                # Extract Main Products
                                main_products = [
                                    p.text for p in (card.eles(".u_FeO") or [])
                                ]

                                # Extract featured products
                                featured_products = []
                                product_elements = card.eles(".Jzokh") or []
                                for prod in product_elements:
                                    try:
                                        price = (
                                            prod.ele(".mNSbN").text
                                            if prod.ele(".mNSbN")
                                            else ""
                                        )
                                        min_order = (
                                            prod.ele(".XYw8w").text
                                            if prod.ele(".XYw8w")
                                            else ""
                                        )
                                        if price:
                                            featured_products.append(
                                                {"price": price, "min_order": min_order}
                                            )
                                    except Exception:
                                        continue

                                supplier_info = {
                                    "company": company_name,
                                    "location": location,
                                    "gold_years": gold_years,
                                    "rating": rating,
                                    "reviews": reviews,
                                    "metrics": metrics,
                                    "main_products": main_products,
                                    "featured_products": featured_products,
                                }

                                all_data.append(supplier_info)
                                print(f"Collected: {company_name}")

                            except Exception:
                                continue

                        # Save Data
                        with open("suppliers_data.json", "w", encoding="utf-8") as f:
                            json.dump(all_data, f, indent=4, ensure_ascii=False)
                        print(f"\nDone! Data saved for {len(all_data)} suppliers.")
                    else:
                        print(
                            "No supplier cards found. Dumping diagnostics to help locate the results container:"
                        )
                        try:
                            candidates = page.eles("section, div") or []
                        except Exception:
                            candidates = []

                        # Print up to 25 candidate containers with a short text sample
                        for i, cand in enumerate(candidates[:25]):
                            try:
                                cls = None
                                try:
                                    cls = cand.attr("class")
                                except Exception:
                                    try:
                                        cls = cand.get_attribute("class")
                                    except Exception:
                                        cls = None
                                txt = cand.text or ""
                                sample = txt.replace("\n", " ")[:140]
                                print(f"  [{i}] class={cls} text_sample={sample}")
                            except Exception:
                                continue
                        print(
                            "End diagnostics. Update selectors or inspect the saved samples above."
                        )
                else:
                    print("Could not find Suppliers tab.")
            else:
                print("Could not find file upload input.")
        else:
            print("Could not find image search button.")

    except Exception as e:
        print(f"Error: {e}")
