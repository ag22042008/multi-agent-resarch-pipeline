from agents import build_search_agent,build_reader_agent,writer_chain,critic_chain
def run_resarch_pipeline(topic:str)->dict:
    state={}# the shared memory
    #search agent working
    print("\n"+" ="*50)
    print("step1->search agent id working...")
    print("="*50)
    search_agent=build_search_agent()
    # if u are invoking an agent you must give in a format specifed in 
    search_result=search_agent.invoke({"messages":[("user",f"Find recent,reliable and information about:{topic}")]})
    state["search_results"]=search_result['messages'][-1].content
    print("\n search result",state["search_results"])
    #2 reader agent
    print("\n"+" ="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)
    reader_agent=build_reader_agent()
    reader_results = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )
        ]
    })
    state['scraped_content']=reader_results['messages'][-1].content
    print("\n scraped content: \n",state['scraped_content'])
    #step3-> writer chain
    print("\n"+"="*50)
    print("Step 3 writer is drafting a report...")
    print("= "*50)
    resarch_combined=(
        f"Search results:\n{state['search_results']}\n\n"
        f"Detailed scraped content:\n{state['scraped_content']}"
    )
    state['report']=writer_chain.invoke({"research":resarch_combined,"topic":topic})
    print("\n Final Report: \n",state['report'])
    #step4-> critic report
    print("\n"+"="*50)
    print("Critic is reviewing the report")
    print("= "*50)
    state['feedback']=critic_chain.invoke({
        "report":state['report']
    })
    print("\n Critic Report: \n",state['feedback'])
    return state# full shared memory returned
if __name__=="__main__":
    topic=input("Enter your resarch topic: ")
    run_resarch_pipeline(topic)





