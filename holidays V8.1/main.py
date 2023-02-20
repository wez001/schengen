from holidays import create_app

app=create_app()    

if __name__=="__main__":    #start the app
    app.run(debug=True)