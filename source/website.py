import json
from typing import Callable

import pandas as pd
import streamlit as st
import base_api as base_api
import data_visualization.language as language
import data_visualization.openaccess as openaccess
import data_visualization.city as city
import data_visualization.subtopic as subtopic
from data_visualization.get_data import get_data, get_embeddings, get_file_index
import data_visualization.subject as subject
import os
import pickle
import glob
from data_visualization import search_paper

st.title("Mineralytics")


def get_trained_subtopics(path_to_models):
    absolute_path = base_api.relative_to_abs(path_to_models)
    pkl_files = glob.glob(os.path.join(absolute_path, "Subtopic_*.pkl"))
    trained_subtopics = [
        os.path.splitext(os.path.basename(f))[0].split("_")[1] for f in pkl_files
    ]
    return trained_subtopics


def get_trained_subject(path_to_models):
    absolute_path = base_api.relative_to_abs(path_to_models)
    pkl_files = glob.glob(os.path.join(absolute_path, "Subject_*.pkl"))
    trained_subject = [
        os.path.splitext(os.path.basename(f))[0].split("_")[1] for f in pkl_files
    ]
    return trained_subject


def load_pickle(path_to_pickle, file_name):
    absolute_path = base_api.relative_to_abs(path_to_pickle)
    if file_name.endswith(".pkl"):
        file_path = os.path.join(absolute_path, file_name)
        try:
            with open(file_path, "rb") as file:
                load_object = pickle.load(file)
            return load_object
        except FileNotFoundError:
            return None
    return None


@st.cache_data
def get_file_content(file: str):
    with open(base_api.relative_to_abs(["data", file])) as file:
        return json.load(file)


if __name__ == "__main__":
    embeddings = get_embeddings()
    data = get_data()

    st.header("langauage")
    language_fig = language.get_fig()
    st.pyplot(language_fig)

    st.write("---")
    
    st.header("open access")
    openaccess_fig = openaccess.get_fig()
    st.plotly_chart(openaccess_fig)

    st.write("---")
    
    st.header("city")
    affiliation_fig = city.get_fig()
    st.plotly_chart(affiliation_fig)

    st.write("---")
    
    st.header("subtopic")
    subtopic_list = data["subtopic"].dropna().unique().tolist()
    trained_subtopics = get_trained_subtopics(
        ["source", "machine_learning", "model", "subtopic"]
    )
    sorted_subtopics = sorted(
        subtopic_list,
        key=lambda x: (
            -1
            if data.loc[data["subtopic"] == x, "subtopic_code"].values[0]
            in trained_subtopics
            else 1
        ),
    )
    selected_subtopic = st.selectbox(
        "Subtopic",
        ["-- Select subtopic --"] + sorted_subtopics,
        placeholder="Select subtopic",
    )
    if selected_subtopic != "-- Select subtopic --":
        subtopic_code = data.loc[
            data["subtopic"] == selected_subtopic, "subtopic_code"
        ].values[0]
        choose = "Subtopic_" + subtopic_code + ".pkl"
        model = load_pickle(["source", "machine_learning", "model", "subtopic"], choose)

        if model:
            subtopic_fig = subtopic.get_fig(selected_subtopic, model)
            st.plotly_chart(subtopic_fig)
        else:
            subtopic_fig = subtopic.get_fig(selected_subtopic)
            st.plotly_chart(subtopic_fig)
            
    st.write("---")
    
    st.header("subject")
    subject_list = data["subject"].dropna().unique().tolist()
    train_subject = get_trained_subtopics(
        ["source", "machine_learning", "model", "subject"]
    )
    sorted_subject = sorted(
        subject_list,
        key=lambda x: (
            -1
            if data.loc[data["subject"] == x, "subject"].values[0] in train_subject
            else 1
        ),
    )
    selected_subject = st.selectbox(
        "Subject",
        ["-- Select subject --"] + sorted_subject,
        placeholder="Select subject",
    )

    if selected_subject != "-- Select subject --":
        subject_code = data.loc[data["subject"] == selected_subject, "subject"].values[
            0
        ]
        choose = "Subject_" + subject_code + ".pkl"
        model = load_pickle(["source", "machine_learning", "model", "subject"], choose)

        if model:
            subject_fig = subject.get_fig(selected_subject, model)
            st.plotly_chart(subject_fig)
        else:
            subject_fig = subject.get_fig(selected_subject)
            st.plotly_chart(subject_fig)

    st.write("---")
    
    st.header("Search Papers From Abstracts")
    prompt = st.text_input("search", value="")
    file_index = get_file_index()
    if prompt != "":
        indices = search_paper.search(prompt)
        for index, result_index in enumerate(indices[0]):
            content = get_file_content(file_index[result_index])
            st.subheader(
                "{}. {}".format(
                    index + 1,
                    content["abstracts-retrieval-response"]["coredata"]["dc:title"],
                )
            )
            st.markdown(
                content["abstracts-retrieval-response"]["item"]["bibrecord"]["head"][
                    "abstracts"
                ]
            )
