# veuszPlugins
My [Veusz](https://github.com/jeremysanders/veusz) plugins.

To export to json, do something like:

```python
dataOut = {}

dataOut["single_value"] = [3]
dataOut["list"] = [1, 2, 3]
dataOut["numpy"] = np.array([1, 2, 3])
dataOut["labels"] = ["label1", "label2"]

out_file = open("data.json","w")
#json.dump(dataOut,out_file,indent=4,sort_keys=True) # plain JSON with the json package
out_file.write(to_json(dataOut))
out_file.flush()
out_file.close()
```
