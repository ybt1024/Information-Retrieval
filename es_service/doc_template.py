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

    job_title = (
        Text()
    )  # by default, Text field will be applied a standard analyzer at both index and search time
    job_post = (
        Text()
    )
    date = (
        Date()
    )
    company_name = (
        Text()
    )
    about_company = (
        Text()
    )
    job_description = (
        Text()
    )
    job_requirement = (
        Text()
    )
    required_Qual = (
        Text()
    )
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
