from elasticsearch_dsl import (  # type: ignore
    Document,
    Text,
    Keyword,
    DenseVector,
    Date,
    token_filter,
    analyzer,
    Nested,
)


class BaseDoc(Document):
    """
    wapo document mapping structure
    """

    doc_id = (
        Keyword()
    )  # we want to treat the doc_id as a Keyword (its value won't be tokenized or normalized).
    title = (
        Text()
    )  # by default, Text field will be applied a standard analyzer at both index and search time
    content = Text(
        analyzer="standard"
    )  # we can also set the standard analyzer explicitly
    stemmed_content = Text(
        analyzer="english"
    )  # index the same content again with english analyzer
    annotation = Nested()
    sbert_embedding = DenseVector(
        dims=768
    )  # sentence BERT embedding in the DenseVector field

    def save(self, *args, **kwargs):
        """
        save an instance of this document mapping in the index
        this function is not called because we are doing bulk insertion to the index in the index.py
        """
        return super(BaseDoc, self).save(*args, **kwargs)


if __name__ == "__main__":
    pass
