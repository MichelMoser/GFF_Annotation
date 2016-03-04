# Tools used to sync and parse gff file

### reformatting webapollo annotations to maker gff standart

Reformatting gff to maker standarts. Column 9 starts with ID=. 
Detailed specifications (see link)

```python rename_apollo_gff.py -in apollo.gff -out apollo.mkr.gff```

### updating old gff file using

Synchronizing new and old annotations.gff. Reporting changes of feature names and checks for duplications.

```python sync_gff.py -in apollo.mkr.gff -old old_annot.gff -out new_annot.gff``` 
