import streamlit as st
from google.cloud import videointelligence
from google.cloud import storage
import json

# Initialize Google Cloud clients
video_client = videointelligence.VideoIntelligenceServiceClient()
storage_client = storage.Client()

# Streamlit app
st.title("AI-Powered Video Indexing")
st.sidebar.header("Options")

# Upload video
uploaded_file = st.file_uploader("Upload a Video File", type=["mp4", "mov", "avi"])

if uploaded_file:
    # Upload video to Google Cloud Storage
    bucket_name = "my-video-bucket05"
    blob_name = uploaded_file.name
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_file(uploaded_file, content_type="video/mp4")

    st.success(f"Uploaded {uploaded_file.name} to {bucket_name}")

    # Analyze video using Google Video Intelligence API
    input_uri = f"gs://{bucket_name}/{blob_name}"
    features = ["LABEL_DETECTION", "SHOT_CHANGE_DETECTION", "TEXT_DETECTION", "SPEECH_TRANSCRIPTION"]

    st.write("Processing video...")
    operation = video_client.annotate_video(request={"input_uri": input_uri, "features": features})
    result = operation.result(timeout=300)

    # Process results
    st.write("**Video Analysis Results:**")
    labels = []
    for annotation in result.annotation_results[0].segment_label_annotations:
        description = annotation.entity.description
        labels.append(description)

    st.write("Labels detected:")
    st.write(", ".join(labels))

    # Search Functionality
    st.write("### Search Functionality")
    search_query = st.text_input("Enter a keyword to search within the video:")
    if search_query:
        matching_labels = [label for label in labels if search_query.lower() in label.lower()]
        if matching_labels:
            st.write(f"Results matching '{search_query}':")
            st.write(", ".join(matching_labels))
        else:
            st.write("No matches found.")
