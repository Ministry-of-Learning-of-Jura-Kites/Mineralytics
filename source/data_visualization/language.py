import source.base_api as base_api
import matplotlib.pyplot as plt
import numpy as np
if __name__ == '__main__':
  lang_column = "abstracts-retrieval-response.language.@xml:lang"
  df = base_api.load_all_data(
      lambda df: df.drop(columns=df.columns.difference([lang_column]))
  )
  # df = base_api.load_data_of_year(
  #     2018,
  #     lambda df: df.drop(
  #         columns=df.columns.difference(
  #             ["abstracts-retrieval-response.language.@xml:lang"]
  #         )
  #     ),
  #     max=100,
  # )

  value_counts = df[lang_column].value_counts()
  plt.bar(
      value_counts.index.to_list(),
      value_counts.values,
  )
  plt.yscale("log",base=2)
  plt.ylabel("count")
  plt.xlabel("language")
  plt.show()
