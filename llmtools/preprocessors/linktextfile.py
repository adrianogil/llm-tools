import os


def preprocess_prompt(prompt):
    # print("Preprocessing prompt: ", prompt)

    result_data = {}

    links = _get_links_from_text(prompt)

    for link in links:
        # print("Link: " + link)
        if os.path.exists(link):
            if link.endswith(".png") or link.endswith(".jpg") or link.endswith(".jpeg"):
                new_prompt_content = f"\nConsider [[{link}]] as a reference for one of the image attached."
                prompt = prompt + new_prompt_content
                result_data["attached_images"] = result_data.get("attached_images", []) + [link]
            else:
                with open(link, 'r') as f:
                    link_content = f.read()
                    new_prompt_content = f"\nConsider [[{link}]] as a reference for the file content below: {link}\n<file-content-start>\n{link_content}\n<file-content-end>\n"
                    prompt = prompt + new_prompt_content
    result_data['prompt'] = prompt
    print(result_data)
    return result_data

def _get_links_from_text(text):
    """
    Get all links from the full content of the page.
    Links are in the format [[link]]
    """
    # print("Getting links from text: ", text)
    links = []
    lines = text.split("\n")
    for line in lines:
        if '[[' in line:
            start = line.find('[[')
            end = line.find(']]')
            link = line[start + 2:end]
            links.append(link)
    return links

