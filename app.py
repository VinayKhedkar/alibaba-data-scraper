"""
AutoSource AI Discovery Engine - Streamlit Dashboard

A web-based interface for automating supplier discovery on Alibaba.com
through AI-powered image search and data scraping.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Add project root to path for imports
import sys
sys.path.append(str(Path(__file__).parent))

from engine.scraper import run_image_search
from utils.helpers import save_uploaded_image, format_supplier_data, cleanup_old_files


# Page configuration
st.set_page_config(
    page_title="AutoSource AI Discovery Engine",
    page_icon="🔍",
    layout="wide"
)


def main():
    """Main application function."""
    
    # Header
    st.title("🔍 AutoSource AI Discovery Engine")
    st.markdown("""
    Upload a product image to automatically discover and compare suppliers on Alibaba.com.
    The system will scrape supplier information including verification status, business history, and response rates.
    """)
    
    # Sidebar for inputs
    st.sidebar.header("Search Parameters")
    
    # Image upload
    st.sidebar.subheader("📸 Product Image")
    uploaded_file = st.sidebar.file_uploader(
        "Upload product image",
        type=['png', 'jpg', 'jpeg', 'webp'],
        help="Upload an image of the product you want to source"
    )
    
    # Numeric inputs
    st.sidebar.subheader("💰 Requirements")
    target_price = st.sidebar.number_input(
        "Target Price (USD)",
        min_value=0.01,
        max_value=1000000.0,
        value=100.0,
        step=10.0,
        help="Your target price per unit"
    )
    
    target_quantity = st.sidebar.number_input(
        "Target Quantity",
        min_value=1,
        max_value=1000000,
        value=1000,
        step=100,
        help="Minimum order quantity you're looking for"
    )
    
    # Inquiry message
    st.sidebar.subheader("✉️ Inquiry Message")
    inquiry_message = st.sidebar.text_area(
        "Message to suppliers",
        value="I am interested in purchasing this product. Please provide your best quote including MOQ, price, and lead time.",
        height=150,
        help="This message will be used when contacting suppliers"
    )
    
    # Search button
    search_button = st.sidebar.button(
        "🚀 Search Suppliers",
        type="primary",
        use_container_width=True
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Search Results")
        
        if search_button:
            if uploaded_file is None:
                st.error("❌ Please upload a product image first!")
            else:
                # Display search parameters
                with st.expander("📋 Search Parameters", expanded=False):
                    st.write(f"**Target Price:** ${target_price:,.2f} USD")
                    st.write(f"**Target Quantity:** {target_quantity:,} units")
                    st.write(f"**Inquiry Message:** {inquiry_message}")
                
                # Save uploaded image
                with st.spinner("💾 Saving uploaded image..."):
                    try:
                        image_path = save_uploaded_image(uploaded_file)
                        st.success(f"✓ Image saved: {Path(image_path).name}")
                    except Exception as e:
                        st.error(f"❌ Error saving image: {e}")
                        return
                
                # Run the scraper
                with st.spinner("🔍 Searching Alibaba for suppliers... This may take a minute."):
                    try:
                        suppliers = run_image_search(image_path)
                        
                        if suppliers:
                            st.success(f"✓ Found {len(suppliers)} suppliers!")
                            
                            # Format and display data
                            formatted_suppliers = format_supplier_data(suppliers)
                            df = pd.DataFrame(formatted_suppliers)
                            
                            # Display as interactive table
                            st.dataframe(
                                df,
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "Supplier Name": st.column_config.TextColumn(
                                        "Supplier Name",
                                        width="large"
                                    ),
                                    "Verified": st.column_config.TextColumn(
                                        "Verified",
                                        width="small"
                                    ),
                                    "Years in Business": st.column_config.TextColumn(
                                        "Years in Business",
                                        width="medium"
                                    ),
                                    "Response Rate": st.column_config.TextColumn(
                                        "Response Rate",
                                        width="medium"
                                    )
                                }
                            )
                            
                            # Download button for CSV export
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Results (CSV)",
                                data=csv,
                                file_name="alibaba_suppliers.csv",
                                mime="text/csv"
                            )
                            
                            # Statistics
                            st.subheader("📊 Statistics")
                            stat_col1, stat_col2, stat_col3 = st.columns(3)
                            
                            with stat_col1:
                                verified_count = sum(1 for s in suppliers if s.get('verified', False))
                                st.metric("Verified Suppliers", verified_count)
                            
                            with stat_col2:
                                avg_years = sum(int(s.get('years_in_business', 0)) for s in suppliers if str(s.get('years_in_business', '')).isdigit()) / len(suppliers) if suppliers else 0
                                st.metric("Avg. Years in Business", f"{avg_years:.1f}")
                            
                            with stat_col3:
                                avg_response = sum(float(s.get('response_rate', 0)) for s in suppliers) / len(suppliers) if suppliers else 0
                                st.metric("Avg. Response Rate", f"{avg_response:.1f}%")
                            
                        else:
                            st.warning("⚠️ No suppliers found. Try a different image or check your connection.")
                            
                    except Exception as e:
                        st.error(f"❌ Error during search: {e}")
                        st.exception(e)
        
        elif not search_button:
            st.info("👆 Upload an image and configure search parameters in the sidebar, then click 'Search Suppliers' to begin.")
    
    with col2:
        st.subheader("Uploaded Image")
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Your product image", use_column_width=True)
        else:
            st.info("No image uploaded yet")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p>AutoSource AI Discovery Engine | Automated Supplier Discovery for Alibaba.com</p>
    <p>⚠️ Note: This tool uses mock data until Playwright authentication is configured.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cleanup old files on app startup (only runs once per session)
    if 'cleanup_done' not in st.session_state:
        cleanup_old_files('data', max_age_hours=24)
        st.session_state.cleanup_done = True


if __name__ == "__main__":
    main()
